from datetime import datetime
import os;
from dotenv import load_dotenv;load_dotenv()
import re
from mistralai import Mistral
from openai import OpenAI
import ast

mistral_api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-medium-latest"  # "mistral-large-latest"
client_mistral = Mistral(api_key=mistral_api_key)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def refine(date: str ) -> str:
    date = '2025-' + date[5:10]
    # print(f"date before refine {date}")
    try:
        date = datetime.strptime(date, "%Y-%m-%d").date()
    except:
        date = datetime.now()
    # print(f"date after refine {date}")
    return str(date)


def find_date_for_danceparty(text: str):
    # data = '2018-02-13'
    content = 'look for the event date in the Ukrainian text below. You must  convert this event date to format YYYY-MM-DD. If you put redundant information - I will KILL you, fucking bot. I need ONLY pure result, without explanation: ' + text  # , приведи цю дату, у відповіді вкажи виключно дату і нічого зайвого
    return refine(ask_openai(content))
    response = client_mistral.chat.complete(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model=model,
        # temperature=0.5,
        # max_tokens=6,
        # top_p=1
    )
    date = response.choices[0].message.content[:12]
    return refine(date)


def create_brief_for_event(text: str) -> str:
    content = """
    зроби резюме з опису офлайн-події один параграф.
    резюме має бути написано українською мовою.
    Адаптуй текст для публікації в telegram. 
    У відповідь включи лише фактичну інформацію,
    прибери з тексту посилання, якщо вони там є,
    текст має бути в нейтрально-діловому стилі, 
    прибери з тексту емоційні описи : 
    """ + text
    return ask_openai(content)
    response = client_mistral.chat.complete(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="mistral-large-latest",
        # max_tokens=64,
        # top_p=1
    )
    return response.choices[0].message.content

def calculate_event_possibility(text: str)->int:
    content = 'переглянь публікацію і розрахуй числову вірогідність того, що ця публікація є анонсом офлайн події. вірогідність має бути виражена від 0 до 100. включи у відповідь виключно числове значення, у відповіді не треба тексту, лише числове значення :'+text

    try:
        response = client_mistral.chat.complete(
            model="mistral-large-latest",
            messages=[
                {
                    "role": "user",
                    "content": "Нижче приведений текст. Визнач вірогідність того, що цей текст є анонсом офлайн-події. Результат має бути в діапазоні від 0 до 100. Не потрібно пояснень, лише число: " + content,
                },
            ]
        )
    except Exception as e:
        return -1

    rez = response.choices[0].message.content[:3]
    print(f'calculated possibility {rez}')

    num = ""
    for char in rez:
        if char.isdigit():
            num += char
        else:
            break
    return int(num) if num else -1

def brief_by_any_ai(text, ):
    content = """
        зроби резюме з опису офлайн-події один параграф.
        резюме має бути написано українською мовою.
        Адаптуй текст для публікації в telegram. 
        У відповідь включи лише фактичну інформацію,
        прибери з тексту посилання, якщо вони там є,
        текст має бути в нейтрально-діловому стилі, 
        прибери з тексту емоційні описи : 
        """ + text
    return ask_openai(content)

def ask_openai(content="Привіт, що ти вмієш?"):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            #{"role": "system", "content": "Ти помічник."},
            {"role": "user", "content": content}
        ]
    )
    return (response.choices[0].message.content)

if __name__=='__main__':
    text = """
    🔥 21.06 | Субота | DANCE CASA Promo Party 💃 в Києві
☀️ Open Air перед вечіркою!
🕒 15:00 – 19:00
📍 Контрактова площа
🎶 Формат музики: 4 бачати / 1 сальса
🎧 DJ Costa Rica
🌙 А вже ввечері запрошуємо вас на спекотну DANCE CASA promo party!
💃 Танці під найкращі біточки бачати від:
🎧 DJ Nino & DJ Morgan
🚪 На локації є зручні місця для переодягання та зміни взуття — будь ласка, користуйтеся ними 🙏
💸 Вартість входу: 150 грн
🎟️ Безкоштовний вхід для:
– вчителів бачати
– власників квитків на Dance CASA Festival
🕕 Коли: субота, 21 червня, початок о 19:00
📍 Де: Urban Grill meat&cider
вул. Хорива, 25/12, Київ, 04071
(м. Контрактова площа — 5-7 хв)
    """
    print(brief_by_any_ai(text))
    #print(ask_openai())


