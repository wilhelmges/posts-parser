print (2+2)
api_id = 29242540
api_hash = '40e13a3d48e04968bf1a31092509feb0'
from telethon.sync import TelegramClient, events

with TelegramClient('vilyashko', api_id, api_hash) as client:
   client.send_message('me', 'Hello, myself!')
   print(client.download_profile_photo('me'))

   @client.on(events.NewMessage(pattern='(?i).*Hello'))
   async def handler(event):
      await event.reply('Hey!')

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