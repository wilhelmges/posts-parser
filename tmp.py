import os
from dotenv import load_dotenv; load_dotenv()# Завантаження змінних середовища
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)
content = '''

💃 Вівторок, 4 березня, 19:30 🕺🏼BACHATA ❤️ SALSA ❤️ KIZOMBA в Buena vista social bar 🎉

✅ 19:30 МК Bachata by
Yurii & Rina, ARdance Project.

💃 Вечірка
🍹 Welcome drink

💰 Вартість 150 грн.

🙋‍♂️ Чекаємо на Вас! 

📌 м. Київ, вул. Велика Житомирська, 8/14.

м. Майдан Незалежності, 
м. Золоті ворота.
'''

chat_response = client.chat.complete(
    model= model,
    messages = [
        {
            "role": "user",
            "content": "Нижче приведений текст. Визнач вірогідність того, що цей текст є анонсом офлайн-події. Результат має бути в діапазоні від 0 до 100. Не потрібно пояснень, лише число: "+content,
        },
    ]
)
print(chat_response.choices[0].message.content)