from PIL import Image, ImageDraw, ImageFont
import textwrap

def add_text_to_image(image_path, output_path, text, font_size=40, font_color=(255, 255, 255)):
    """
    Додає текст на зображення по центру.
    
    Args:
        image_path (str): Шлях до вхідного зображення
        output_path (str): Шлях для збереження результату
        text (str): Текст для додавання
        font_size (int): Розмір шрифту
        font_color (tuple): Колір тексту у форматі RGB
    """
    # Відкриваємо зображення
    img = Image.open(image_path)
    
    # Створюємо об'єкт для малювання
    draw = ImageDraw.Draw(img)
    
    # Завантажуємо шрифт
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", font_size)
    except:
        # Якщо шрифт не знайдено, використовуємо стандартний
        font = ImageFont.load_default()
    
    # Отримуємо розміри зображення
    img_width, img_height = img.size
    
    # Розбиваємо довгий текст на рядки
    max_width = int(img_width * 0.8)  # Використовуємо 80% ширини зображення
    lines = textwrap.wrap(text, width=int(max_width / (font_size * 0.6)))
    
    # Розраховуємо загальну висоту тексту
    line_height = font_size + 5
    text_height = len(lines) * line_height
    
    # Розраховуємо початкову y-координату для центрування тексту
    y = (img_height - text_height) / 2
    
    # Додаємо кожен рядок тексту
    for line in lines:
        # Отримуємо ширину конкретного рядка
        line_width = draw.textlength(line, font=font)
        # Розраховуємо x-координату для центрування
        x = (img_width - line_width) / 2
        
        # Додаємо тінь для кращої читабельності
        draw.text((x+2, y+2), line, font=font, fill=(0, 0, 0))
        # Додаємо основний текст
        draw.text((x, y), line, font=font, fill=font_color)
        
        y += line_height
    
    # Зберігаємо результат
    img.save(output_path)

if __name__ == "__main__":
    # Приклад використання
    add_text_to_image(
        "sample01.png",
        "output.png",
        "10-12 січня",
        font_size=120,
        font_color=(0, 0, 255)
    ) 