from quart import Quart, render_template, jsonify
from quart_cors import cors
from telethon import TelegramClient, events
import os
from dotenv import load_dotenv
from post_processor import calculate_event_possibility
from repository import supabase
import datetime
from publisher import prepare_posts
import time, datetime, locale

load_dotenv()# Завантаження змінних середовища

# Налаштування Telegram клієнта
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
client = TelegramClient('vilyashko', api_id, api_hash)

# Створення Quart додатку
app = Quart(__name__)
app = cors(app)

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/api/scan')
async def scan_sources():
    POST_LIMIT = 10
    """Ендпоінт для сканування джерел контенту"""
    try:
        # Додати визначення category
        category = 'dance'  # або отримати з параметрів запиту
        
        if not client.is_connected():
            await client.connect()
            
        current_date =(datetime.date.today())
        kyivdancesources = supabase.table('sources').select("id, slug,media, topic, city").eq('media', 'telega').eq('category',category).limit(20).execute().data
        added = 0
        possibilities = []
        for source in kyivdancesources:
            print(source['slug'])

            if source['topic']:
                messages = await client.get_messages(source['slug'], reply_to=source['topic'], limit=POST_LIMIT)
            else:
                messages = await client.get_messages(source['slug'], limit=POST_LIMIT)

            for message in messages:
                if message.text:
                    #print(dir(message)); exit()
                    text = (message.message).replace("\n", ". ")
                    post_date= (message.date).date()
                   
                    if (current_date - post_date).days>6:
                        break
                    if len(text)<10:
                        continue
                    _hash = hash((message.id, message.chat_id))
                    possibility = calculate_event_possibility(text)
                    
                    post_to_save = {"fulltext": text, "source_slug": source['slug']+':'+source['media'], "category": category,"city":source['city'], 'status': 'notreviewed', "hash": _hash, "possibility": possibility}
                    print(possibility, text[:40])
                    try: 
                        supabase.table('posts').insert(post_to_save).execute()
                        added += 1
                    except Exception as e:
                        print(f"Помилка при збереженні посту: {e}")
                        continue

        return jsonify({
            "status": "success",
            "added": added,
        })
        
    except Exception as e:
        print(f"Детальна помилка: {str(e)}")  # додати для кращого логування
        return jsonify({
            "status": "error",
            "message": f"error: {str(e)}"
        }), 500

@app.route('/api/getsummaries')
async def getsummaries():
    """Ендпоінт для отримання резюме анонсів"""
    try:
        processed = prepare_posts()
        return jsonify({
            "status": "success",
            "processed": processed
        })

    except Exception as e:
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
        locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
        current = datetime.date.today()
        response = []
        group = 'https://t.me/opendance_life'
        cities = {"Київ":69523, "Дніпро": 75286 , "Львів": 75292, "Одеса": 75294, "Тернопіль":75417} #,
        for city in  cities:
            topic = cities[city]
            response = supabase.table('posts').select(
                "fulltext, event_date, brief, id").eq('status', 'readytopost').eq('city',city).eq('category', 'dance').gte('event_date', str(current)).order('event_date', desc=False).limit(20).execute().data
            print(city, topic, len(response))
            if len(response)<1:
                continue
            print('publishing '+city)

            client.parse_mode = 'html'
            digest = 'дайджест вечірок на тиждень \n\n'
            for repost in response:
                event_date = datetime.datetime.strptime(repost['event_date'], "%Y-%m-%d")
                text = repost['brief'] if repost['brief'] else repost['fulltext']
                digest = digest + f"<b>{event_date.strftime('%A - %d %B')}</b>\n {text}\n\n"
            if city=="Київ":
                digest = digest + f"<b> анонси вечірок у Львові, Дніпрі, Одесі, Тернополі, Києві ви можете подивитись в групі https://t.me/opendance_life, також тут можна глянути анонси нових танцювальних наборів і танцювальні фестивалі"
            print(digest)
            await client.send_message(entity=group, reply_to=topic, message=digest)

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
    app.run(debug=(True if os.getenv('USER')=='rasser' else False)) 