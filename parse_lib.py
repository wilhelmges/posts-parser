from telethon import TelegramClient
from telethon.sync import TelegramClient as tcsync

api_id = 14535551 #app1
api_hash = 'ee049ec9130de53ec5336fe819e49365'

def parse_channel(session, groupid, limit=3):
    with tcsync(session, api_id, api_hash) as client:
        messages = client.get_messages(groupid, limit=limit)
        return messages

def parse_topic(session, groupid, topicid, limit=3):
    with tcsync(session, api_id, api_hash) as client:
        # entity = client.get_input_entity('https://t.me/opendance_life'); print(type(entity))
        messages = client.get_messages(groupid, reply_to=topicid, limit=limit)
        return messages