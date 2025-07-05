import os
import datetime, time, traceback
from telethon import TelegramClient
from telethon.tl.types import InputPeerChannel

from services.repository import supabase
from services.post_processor import calculate_event_possibility

from dotenv import load_dotenv; load_dotenv()
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
client = TelegramClient('vvn', api_id, api_hash)

async def main(category='dance', post_limit=7):
    added = 0
    current_date = datetime.date.today()

    if not client.is_connected():
        await client.connect()

    sources = supabase.table('sources').select("channel_id,slug,topic").eq('category', category).eq('media', 'telega').eq('city','Київ').limit(20).execute().data #

    kyivdanceids = [item['channel_id'] for item in sources] #; print (kyivdanceids)
    # "slug,channel_id, access_hash, media, city"
    # sources = [{"slug":"https://t.me/c/1435154608/62400"}]

    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        entity = dialog.entity
        print(f"{dialog.name} - ID: {entity.id}")
        if entity.id not in kyivdanceids:
            continue
        result = next((channel for channel in sources if channel['channel_id'] == entity.id), None); print(result)
        print('here dancing media');
        # messages = await client.get_messages(entity, limit=post_limit)
        messages = await client.get_messages(entity, reply_to=result['topic'], limit=post_limit) if 'topic' in result and result[
            'topic'] else await client.get_messages(entity, limit=post_limit)
        #print(len(messages));continue

        for message in messages:
            if not message.text:
                continue
            text = message.message.replace("\n", ". ")
            post_date =  message.date.date()
            if (current_date - post_date).days > 6 or len(text) < 10:
                continue
            print(text[:40], post_date)

            _hash = hash((message.id, message.chat_id))
            #we need to check if this record was inserted already
            post_data = {
                "fulltext": text,
                "source_slug": f"{dialog.name}:telega",
                "category": category,
                "city": 'Київ',
                "status": "notreviewed",
                "hash": _hash,
            }

            try:
                supabase.table('posts').insert(post_data).execute()#if error - this record was added to db before
                time.sleep(10)
                possibility = calculate_event_possibility(text)
                supabase.table('posts').update({"possibility": possibility}).eq("hash", _hash).execute()
                added += 1
            except Exception:
                traceback.print_exc()

    return added

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())