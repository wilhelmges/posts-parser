import http.server
import socketserver
import argparse
import json
from urllib.parse import urlparse
from publisher import prepare_posts

# Значення порту за замовчуванням
DEFAULT_PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    # Константи класу
    DANCE_CATEGORY = 'dance'
    API_PREFIX = '/api/'
    
    def set_cors_headers(self):
        """Встановлення стандартних CORS заголовків"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')

    def send_json_response(self, status_code, data):
        """Відправка JSON відповіді з CORS заголовками"""
        self.send_response(status_code)
        self.set_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def handle_api_request(self, endpoint):
        """Обробка API запитів"""
        # Мапінг ендпоінтів на їх обробники
        endpoints = {
            'parse': self._handle_parse,
            'needsummary': self._handle_summary,
            'publish': self._handle_publish
        }
        
        handler = endpoints.get(endpoint)
        if not handler:
            return False
            
        try:
            response_data = handler()
            self.send_json_response(200, response_data)
            return True
        except Exception as e:
            self.send_json_response(500, self._create_error_response(str(e)))
            return True
    
    def _handle_parse(self):
        """Обробка запиту на парсинг"""
        result = prepare_posts(self.DANCE_CATEGORY, parse_only=True)
        return {"status": "success", "data": result}
    
    def _handle_summary(self):
        """Обробка запиту на створення підсумків"""
        processed = prepare_posts(self.DANCE_CATEGORY)
        return {"status": "success", "processed": str(processed)}
    
    def _handle_publish(self):
        """Обробка запиту на публікацію"""
        published_data = prepare_posts(self.DANCE_CATEGORY, publish_only=True)
        return {
            "status": "success",
            "message": "Публікацію успішно опубліковано",
            "data": published_data
        }
    
    @staticmethod
    def _create_error_response(message):
        """Створення стандартної відповіді про помилку"""
        return {"status": "error", "message": message}

    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path.startswith(self.API_PREFIX):
            endpoint = parsed_path.path[len(self.API_PREFIX):]
            if self.handle_api_request(endpoint):
                return
                
        super().do_GET()

    def do_OPTIONS(self):
        self.send_response(200)
        self.set_cors_headers()
        self.end_headers()

def start_server(port):
    try:
        handler = CustomHandler
        httpd = socketserver.TCPServer(("", port), handler)
        print(f"Сервер запущено на порту {port}")
        print(f"API доступне за адресою: http://localhost:{port}/api/needsummary")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер зупинено.")
        httpd.shutdown()
        httpd.server_close()
    except Exception as e:
        print(f"\nПомилка сервера: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Простий Python сервер зі статичними файлами та API.")
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Порт для запуску сервера (за замовчуванням: {DEFAULT_PORT})"
    )
    args = parser.parse_args()
    start_server(args.port)
