import os
import datetime, time, traceback
from telethon import TelegramClient
# from repository import supabase
# from post_processor import calculate_event_possibility

from dotenv import load_dotenv; load_dotenv()
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
client = TelegramClient('vilyashko', api_id, api_hash)

async def main(category='dance', post_limit=5):
    added = 0
    current_date = datetime.date.today()

    if not client.is_connected():
        await client.connect()

    # sources = supabase.table('sources').select("*").eq('category', category).eq('media', 'telega').limit(
    #     20).execute().data
    sources = [{"slug":"latinpartyinkyiv"}]

    for source in sources:
        messages = await client.get_messages(source['slug'], reply_to=source['topic'], limit=post_limit) if 'topic' in source and source[
            'topic'] else await client.get_messages(source['slug'], limit=post_limit)


        for message in messages:
            if not message.text:
                continue
            text = message.message.replace("\n", ". ")
            post_date = message.date.date()
            if (current_date - post_date).days > 6 or len(text) < 10:
                continue
            print(text[:40], post_date); continue

            _hash = hash((message.id, message.chat_id))
            post_data = {
                "fulltext": text,
                "source_slug": f"{source['slug']}:{source['media']}",
                "category": category,
                "city": source['city'],
                "status": "notreviewed",
                "hash": _hash,
            }

            try:
                supabase.table('posts').insert(post_data).execute()
                time.sleep(10)
                possibility = calculate_event_possibility(text)
                supabase.table('posts').update({"possibility": possibility}).eq("hash", _hash).execute()
                added += 1
            except Exception:
                traceback.print_exc()

    return {"status": "success", "added": added}

with client:
    client.loop.run_until_complete(main())