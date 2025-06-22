from quart import Quart, render_template, jsonify
from quart_cors import cors
from telethon import TelegramClient
from telegram import Bot
import os
from babel.dates import format_datetime

from publisher import prepare_posts
from services.post_processor import calculate_event_possibility
from services.repository import supabase
from services.scan_tgsources import main as sts
from publisher import prepare_posts as pp
import datetime
from dotenv import load_dotenv; load_dotenv()# Завантаження змінних середовища
import traceback
import time

# Налаштування Telegram клієнта
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
client = TelegramClient('vilyashko', api_id, api_hash)
# Use this if you're authenticating as a bot
bot = Bot(os.getenv('DANCEDIGEST_BOT_TOKEN'))

app = Quart(__name__)# Створення Quart додатку
app = cors(app)

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/api/scan')
async def scan_sources():
    POST_LIMIT = 10
    """Ендпоінт для сканування джерел контенту"""
    category = 'dance'  # або отримати з параметрів запиту # Додати визначення category

    try:
        added = await sts(category=category, post_limit=POST_LIMIT)
        return jsonify({
            "status": "success",
            "added": added
        })
        
    except Exception as e:
        print(f"Детальна помилка: {str(e)} {e}")  # додати для кращого логування
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": f"error: {str(e)}"
        }), 500

@app.route('/api/prepare_posts')
async def prepare_posts():
    """Ендпоінт для отримання резюме анонсів"""
    try:
        processed = pp()
        return jsonify({
            "status": "success",
            "processed": processed
        })

    except Exception as e:
        print(str(e))
        return jsonify({
            "status": "error",
            "message": f"error: {str(e)}"
        }), 500
    
@app.route('/api/publishdigests')
async def publishdigests():
    """Ендпоінт для публікації дайджесту"""
    try:
        if not client.is_connected():
            await client.connect()

        #locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8') #uk_UA.UTF-8 unsupported in render.com
        current = datetime.date.today()
        response = []
        group = '@opendance_life'
        cities = {"Київ":69523} #, "Дніпро": 75286 , "Львів": 75292, "Одеса": 75294, "Тернопіль":75417} #,
        for city in  cities:
            topic = cities[city]
            response = supabase.table('posts').select(
                "fulltext, event_date, brief, id").eq('status', 'readytopost').eq('city',city).eq('category', 'dance').gte('event_date', str(current)).order('event_date', desc=False).limit(20).execute().data
            print(city, topic, len(response))
            if len(response)<1:
                continue
            print('publishing '+city)

            client.parse_mode = 'html'
            num = 1
            digest = 'дайджест вечірок на тиждень \n'
            if city == "Київ":
                digest = digest + f"💃🕺🏻 повні анонси вечірок у Києві🏛️, Вінниці⚓, Хмельницькому🏹 <strong>анонси ноборів в студії</strong>,  ви можете подивитись в групі <a href='https://t.me/opendance_life'>чат з танців</a>, також тут можна глянути анонси про танцювальні фестивалі\n\n"
                # digest = digest + f" також ви можете відстежувати <b>анонси подій в instagram</b> https://www.instagram.com/vitodancedigest/"

            for repost in response:
                print(num, repost['brief'][:35])
                event_date = datetime.datetime.strptime(repost['event_date'], "%Y-%m-%d")
                formatted_date = format_datetime(event_date, "EEEE, d MMMM ", locale="uk")
                text = repost['brief'] if repost['brief'] else repost['fulltext']
                digest = digest + f"<strong>{formatted_date}</strong>\n {text}\n\n"
            print(digest)

            try:
                #await bot.send_message(chat_id='@test_tg_api_polytopic', message_thread_id=1, text='12345')
                #TODO: need to be fixed for other locations
                await bot.send_message(chat_id="@opendance_life", message_thread_id=77971, text=digest, parse_mode="HTML")
            except Exception as e:
                print(e, str(e))

        return jsonify({
            "status": "success",
            "message": "Дайджест опубліковано"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"error: {str(e)}"
        }), 500

@app.route('/hello')
async def hello_world():
    return 'Hello from Quart!'

if __name__ == '__main__':
    client.loop.run_until_complete(app.run())
    #client.loop.run_until_complete(app.run(debug=(True if os.getenv('USER')=='rasser' else False)))
    #app.run(debug=(True if os.getenv('USER')=='rasser' else False))