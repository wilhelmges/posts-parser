import os
from dotenv import load_dotenv; load_dotenv()# Завантаження змінних середовища
from telethon import TelegramClient, events
from telethon.tl.types import InputPeerChannel


api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
client = TelegramClient('vvn', api_id, api_hash)

async def main():

    peer = InputPeerChannel(1406630718,  8353212268835877625)
    print(dir(peer))
    messages = await client.get_messages(peer, limit=3)
    print(messages)
    # print(dialog.id, dialog.name, dialog.entity)
    # entity = await client.get_entity('https://t.me/+fDwTcGlT7Pw0ZTEy ')
    # # https://t.me/ethkyiv_ua https://t.me/improvisationschoolua
    # messages  = await client.get_messages(entity, limit=2)
    # print(messages)


with client:
        client.loop.run_until_complete(main())