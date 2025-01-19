import os; from dotenv import load_dotenv; load_dotenv()

from telethon import TelegramClient

api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')

dancedigest_bot_token =  os.getenv('DANCEDIGEST_BOT_TOKEN')  # Use this if you're authenticating as a bot
client = TelegramClient('bot', api_id, api_hash).start(bot_token=dancedigest_bot_token)
async def send_message_to_topic(message):
    await client.send_message("https://t.me/test_tg_api_polytopic", message, reply_to=1)

with client:
    client.loop.run_until_complete(send_message_to_topic("5 Hello, this is a test message from Telethon!"))
