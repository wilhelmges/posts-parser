from openai import OpenAI
from datetime import datetime
import os; from dotenv import load_dotenv; load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAPI"))

def refine(date:str='18.02')->str:
    date ='2025-' + date[5:]
    return date
    date = datetime.strptime(date, "%Y.%d.%m").date()
    return str(date)

def find_date_for_danceparty(text: str):
    # data = '2018-02-13'
    content = 'look for the event date in the Ukrainian text below. You must  convert this event date to format YYYY-MM-DD. If you put redundant information - I will KILL you, fucking bot. I need ONLY pure result, without explanation: ' + text #, приведи цю дату, у відповіді вкажи виключно дату і нічого зайвого
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="gpt-3.5-turbo",
        # temperature=0.5,
        max_tokens=6,
        # top_p=1
    )
    date = response.choices[0].message.content[:12]
    return refine(date)


def create_brief_for_event(text: str)->str:
    content = 'зроби резюме з опису офлайн-події один параграф. резюме має бути написано українською мовою. Адаптуй текст для публікації в telegram. У відповідь включи лише фактичну інформацію, текст має бути в нейтрально-діловому стилі, прибери з тексту емоційні описи : ' + text
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="gpt-3.5-turbo",
        # max_tokens=64,
        # top_p=1
    )
    return response.choices[0].message.content

def calculate_event_possibility(text: str)->str:
    content = 'переглянь публікацію і розрахуй числову вірогідність того, що ця публікація є анонсом офлайн події. вкажи вірогідність як результат. вірогідність має бути виражена від 0 до 100. включи у відповідь виключно цифри, нічого зайвого. не треба пояснень, лише числове значення :'+text
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return int(response.choices[0].message.content)

if __name__=='__main__':
    text = '''
One love - то три зали на 600 м2, в цю неділю танцюємо в Nivki Hall 🤩

👉 3 великих зали на кожен стиль:
 • БАЧАТА
🎧 качає Dj Raul
 • САЛЬСА Cuban
🎧 запалює Dj  Sanchez
 • ЗУК
🎧 за пультом Dj Yan

📆 Коли: 18.02 (неділя) 19:00-22:00
📍 Де: Nivki Hall, проспект Берестейський, 84 

💰Вхід: 200грн

Вриваємося в цей вечір 😍
    '''
    print(calculate_event_possibility(text))