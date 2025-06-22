from telethon.sync import TelegramClient
from services.repository import supabase
import time, datetime, locale
from services.post_processor import find_date_for_danceparty, create_brief_for_event

api_id = 14535551; api_hash = 'ee049ec9130de53ec5336fe819e49365' # app1

def prepare_posts(topic='dance'):
    current = datetime.date.today()
    responce = supabase.table('posts').select("fulltext, id, created_at, source_slug").eq('status','needsummary').eq('category',topic).order('created_at', desc=True).limit(15).execute().data #.is_('brief', 'null')
    processed = 0
    for repost in responce:
        text = repost['fulltext']
        # print(repost['created_at'], text[:40])
        try:
            print( text[:25], repost['source_slug'], repost['id']);
            time.sleep(7)
            date = find_date_for_danceparty(text)
            print(date)
            time.sleep(7)
            brief = create_brief_for_event(text)
            print(brief,)
            data, count = supabase.table('posts').update({'event_date': date, 'brief':brief}).eq('id', repost['id']).execute()
            processed += 1
        except Exception as e:
            print(str(e))
    
    return processed

def publish_dance_parties():
    locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
    current = datetime.date.today()
    response = []
    group = 'https://t.me/opendance_life'
    cities = {"Київ":69523, "Дніпро": 75286 , "Львів": 75292, "Одеса": 75294, "Тернопіль":75417} #,
    for city in  cities:
        topic = cities[city]
        response = supabase.table('posts').select(
            "fulltext, event_date, brief, id").eq('status', 'torepost').eq('city',city).eq('category', 'dance').gte('event_date', str(current)).order('event_date', desc=False).limit(20).execute().data
        print(city, topic, len(response))
        if len(response)<1:
            continue
        print('publishing '+city)
        with TelegramClient('vilyashko', api_id, api_hash) as client:
            client.parse_mode = 'html'
            digest = 'дайджест вечірок на тиждень \n\n'
            for repost in response:
                event_date = datetime.datetime.strptime(repost['event_date'], "%Y-%m-%d")
                text = repost['brief'] if repost['brief'] else repost['fulltext']
                digest = digest + f"<b>{event_date.strftime('%A - %d %B')}</b>\n {text}\n\n"
            if city=="Київ":
                digest = digest + f" також ви можете відстежувати анонси подій в instagram https://www.instagram.com/vitodancedigest/"
                #digest = digest + f"<b> анонси вечірок у Львові, Дніпрі, Одесі, Тернополі, Києві ви можете подивитись в групі https://t.me/opendance_life, також тут можна глянути анонси нових танцювальних наборів і танцювальні фестивалі"
            print(group);print(topic);
            client.send_message(entity=group, reply_to=topic, message=digest)


def iterate_reposts(topic='test'):
    locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
    current = datetime.date.today(); response=[]
    match topic:
        case 'test': group = 'https://t.me/test_tg_api_polytopic' ; topic = 1; response = supabase.table('posts').select("text,event_date, event_brief, id").eq('status','torepost').gte('event_date', str(current)).order('event_date', desc=False).limit(10).execute().data

        case 'culture':
            group = 'https://t.me/opendance_life' ; topic = 73360; response = supabase.table('posts').select("text,event_date, event_brief, source, id").eq('status','torepost').eq('category','culture').gte('event_date', str(current)).order('event_date', desc=False).limit(20).execute().data
            with TelegramClient('vilyashko', api_id, api_hash) as client:
                client.parse_mode = 'html'
                digest = 'дайджест подій на тиждень \n\n'
                for repost in response:
                    event_date = datetime.datetime.strptime(repost['event_date'], "%Y-%m-%d")

                    text = repost['event_brief'] if repost['event_brief'] else repost['text']
                    digest = digest + f" <b>{event_date.strftime('%A - %d %B')}</b>\n {text}. source: {repost['source']}\n\n"
                client.send_message(entity=group, reply_to=topic, message=digest)

if __name__ == "__main__":
    pass
    # publish_dance_parties()
    # iterate_reposts('culture')
    # iterate_reposts('testdance')

    prepare_posts('dance');
    # prepare_posts('culture')

def msg_test():
    with TelegramClient('vilyashko', api_id, api_hash) as client:
        # client.send_message('helvetian', 'Hello, little boss!')
        for i in range(10):
            client.send_message(entity=group, reply_to=1, message=str(10-i)+" bottles of juice on the table")
            time.sleep(1)

        # case 'dancekyiv':
        #     group = 'https://t.me/test_tg_api_polytopic'; topic = 4; response = supabase.table('posts').select(
        #         "text, event_date, event_brief, id").eq('status', 'torepost').eq('category','dancekyiv').gte('event_date', str(current)).order('event_date', desc=False).limit(9).execute().data
        #     with TelegramClient('vilyashko', api_id, api_hash) as client:
        #         client.parse_mode = 'html'
        #         digest = 'дайджест вечірок на тиждень \n\n'
        #         for repost in response:
        #             event_date = datetime.datetime.strptime(repost['event_date'], "%Y-%m-%d")
        #             text = repost['event_brief'] if repost['event_brief'] else repost['text']
        #             digest = digest +  f"<b>{event_date.strftime('%A - %d %B')}</b>\n {text}\n\n"
        #         client.send_message(entity=group, reply_to=topic, message=digest)
