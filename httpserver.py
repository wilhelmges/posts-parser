import http.server
import socketserver
import argparse

# Значення порту за замовчуванням
DEFAULT_PORT = 8000

def start_server(port):
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving static files on port {port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            httpd.shutdown()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Python static file server.")
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port to run the server on (default: {DEFAULT_PORT})"
    )
    args = parser.parse_args()
    start_server(args.port)
