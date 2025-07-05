from apify_client import ApifyClient
import os
import datetime, time, traceback
from services.repository import supabase
from services.post_processor import calculate_event_possibility

from dotenv import load_dotenv; load_dotenv()
apifi_key = os.getenv('APIFY_API_KEY')
client = ApifyClient(apifi_key)

def main(category='dance'):
    added = 0
    current_date = datetime.datetime.today()
    sources = supabase.table('sources').select("slug").eq('category', category).eq('media', 'insta').eq('city','Київ').limit(20).execute().data #
    slug_values = [item['slug'] for item in sources]
    print(slug_values)
    # print(sources); exit()
    rez = get_last_insta_posts(profiles=slug_values, items=6)

    for message in rez:
        text = message['caption'].replace("\n", ". ")
        if not text or len(text) < 10:
            continue
        post_date = datetime.datetime.strptime(message['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if (current_date - post_date).days > 6 :
            pass #continue

        print(message['caption'][:30], post_date, message['shortCode'], message['id'])


        #_hash = hash((message.id, message.chat_id))
        # we need to check if this record was inserted already
        post_data = {
            "id":message['id'],
            "fulltext": text,
            "source_slug": '-'+":insta",
            "category": category,
            "city": 'Київ',
            "status": "notreviewed",
        }

        try:
            supabase.table('posts').insert(post_data).execute()  # if error - this record was added to db before
            time.sleep(10)
            possibility = calculate_event_possibility(text)
            supabase.table('posts').update({"possibility": possibility}).eq("id", message['id']).execute()
            added += 1
        except Exception:
            traceback.print_exc()


def get_last_insta_posts(profiles, items = 1 ):
    # from sdata import items; return items
    # Prepare the Actor input
    run_input = {
        "username": profiles,
        "resultsLimit": items,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("apify/instagram-post-scraper").call(run_input=run_input)
    rez=[]
    # Fetch and print Actor results from the run's dataset (if there are any)
    print("💾 Check your data here: https://console.apify.com/storage/datasets/" + run["defaultDatasetId"])
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        rez.append(item)
        #print(item)

    return rez

if __name__=='__main__':
    main()
    #print(get_last_insta_posts(profiles=["lagofamilykyiv","salsahubkyiv"]))
