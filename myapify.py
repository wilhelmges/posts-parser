from apify_client import ApifyClient
import os
import datetime, time, traceback
from services.repository import supabase
from services.post_processor import calculate_event_possibility

from dotenv import load_dotenv; load_dotenv()
apifi_key = os.getenv('APIFY_API_KEY')
client = ApifyClient(apifi_key)

def main(category='dance', items=1, city="Київ"):
    added = 0
    current_date = datetime.datetime.today()
    sources = supabase.table('sources').select("slug").eq('category', category).eq('media', 'insta').eq('city',city).limit(20).execute().data #
    slug_values = [item['slug'] for item in sources]
    print(slug_values)# print(sources); exit()
    rez = get_last_insta_posts(profiles=slug_values, items=items)

    for message in rez:
        text = message['caption'].replace("\n", ". ")
        if not text or len(text) < 10:
            continue
        post_date = datetime.datetime.strptime(message['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if (current_date - post_date).days > 7 :
            pass #continue
        print(message['caption'][:30], post_date, message['shortCode'], message['id'])
        _hash = hash((message.id, message.chat_id))
        # we need to check if this record was inserted already
        post_data = {
            # problems with receiving in js "id":message['id'],
            "fulltext": text,
            "source_slug": message['source'],
            "category": category,
            "city": city,
            "status": "notreviewed",
            "hash": _hash,
        }

        try:
            supabase.table('posts').insert(post_data).execute()  # if error - this record was added to db before
            time.sleep(10)
            possibility = calculate_event_possibility(text)
            supabase.table('posts').update({"possibility": possibility}).eq("id", message['id']).execute()
            added += 1
        except Exception:
            traceback.print_exc()

def temp_provider():
    return
    [
        {
            "caption": "Це точно 🚫НЕ кізомба.\nБачата в обіймах? 🧐Сплячі пари на танцполі?😅\nЗабудь усе, що ти думав про кізомбу — зараз буде по-справжньому.\n\n🎥 Частина 1 з 3 — далі буде ще цікавіше.\n\n#танці #socialdance #kizomba #afrodance #urbankiz #танцюйзнами #вритмі #танцюйсерцем #рілз #dancevideo #dancersofinstagram #українськітанці #kizombaflow #африкавсерці #kizombaislife",
            "ownerFullName": "Yevhen_Lee",
            "ownerUsername": "yevhen_lee",
            "url": "https://www.instagram.com/p/DLzsIa9ikyl/",
            "commentsCount": 13,
            "firstComment": "😍😍😍топ!",
            "likesCount": 87,
            "timestamp": "2025-07-07T13:09:28.000Z"
        },
        {
            "caption": "Чому соціальні танці були і будуть популярними❓\nБо вони об’єднують.\nРізних людей. Різні характери.\nВ одне — танцювальне Комʼюніті ❤️\n\nІ я не хочу розділяти його на “Сальса тут”, “Бачата там”.\nЦі стилі доповнюють одне одного:\n👉 Чого нема в Бачаті — є в Сальсі\n👉 Чого нема в Сальсі — є в Бачаті\n\nАле зараз, на жаль:\nСальса окремо…\nБачата окремо…\n\nА анімації — це саме той формат, який може нас знову обʼєднати.\nПоказати, заради чого ми всі тут.\nРух. Спільність. Радість.\n\nМожливо, хтось вже забув, що таке анімація.\nМожливо, нові танцівники навіть не знають, що це.\nМожливо, школи забороняють танцювати “під чужих викладачів”.\n\nАле танець — не про заборони.\nТанець — це свобода.\nІ зараз, коли багатьом важко, саме танці тримають нас у житті.\n\nПідтримуйте анімації.\nТанцюйте разом.\nБо в цьому — наша сила. ❤️🔥\n\n#salsakyiv #bachatakyiv #анімація #bailaclubkyiv #сальсабачата #танціобʼєднують #соціальнітанці",
            "ownerFullName": "Ксенія Петренко | SALSA•BACHATA |",
            "ownerUsername": "ksenia_latindancer",
            "url": "https://www.instagram.com/p/DLzMlAbtOEG/",
            "commentsCount": 4,
            "firstComment": "Супер!!!!",
            "likesCount": 98,
            "timestamp": "2025-07-07T08:33:42.000Z"
        }
    ]

def get_last_insta_posts(profiles, items = 1 ):
    # from sdata import items; return items
    rez = []
    for profile in profiles:
        run_input = {
            "username": [profile],
            "resultsLimit": items,
        }
        run = client.actor("apify/instagram-post-scraper").call(run_input=run_input)
        items0 = [item for item in client.dataset(run["defaultDatasetId"]).iterate_items()]
        print("💾 Check your data here: https://console.apify.com/storage/datasets/" + run["defaultDatasetId"])
        for item0 in items0:
            item = item0; item['source']='insta: '+profile
            rez.append(item)
    return rez

if __name__=='__main__':
    main(items=3)
    #print(get_last_insta_posts(profiles=["lagofamilykyiv","salsahubkyiv"]))
