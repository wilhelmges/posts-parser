print (2+2)
import os
from dotenv import load_dotenv; load_dotenv()# Завантаження змінних середовища
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
from telethon.sync import TelegramClient, events

with TelegramClient('vilyashko', api_id, api_hash) as client:
   client.send_message('me', 'Hello, myself!')
   me = client.get_me()
   print(me.id, me.username)
   dialogs = client.get_dialogs(limit=1)
   print(dialogs)


   # @client.on(events.NewMessage(pattern='(?i).*Hello'))
   # async def handler(event):
   #    await event.reply('Hey!')

   client.run_until_disconnected()
# import os
# from dotenv import load_dotenv; load_dotenv()# Завантаження змінних середовища
# from telethon import TelegramClient, events
# api_id = int(os.getenv('TELEGRAM_API_ID'))
# api_hash = os.getenv('TELEGRAM_API_HASH')
# client = TelegramClient('vvn', api_id, api_hash)
#
#
#
# async def main():
#     entity = await client.get_entity('https://t.me/+fDwTcGlT7Pw0ZTEy ')
#     # https://t.me/ethkyiv_ua https://t.me/improvisationschoolua
#     messages  = await client.get_messages(entity, limit=2)
#     print(messages)
#
#
# with client:
#         client.loop.run_until_complete(main())

# for source in sources:
#     messages = await client.get_messages(source['slug'], reply_to=source['topic'],
#                                          limit=post_limit) if 'topic' in source and source[
#         'topic'] else await client.get_messages(source['slug'], limit=post_limit)