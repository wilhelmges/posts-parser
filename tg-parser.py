from telethon.sync import TelegramClient
from parse_lib import parse_topic, parse_channel
from repository import supabase
import datetime
import re

api_id = 14535551 #app1
api_hash = 'ee049ec9130de53ec5336fe819e49365'

def grab_groups():
    c=0

    with TelegramClient('vilyashko', api_id, api_hash) as client:
        for dialog in client.iter_dialogs():
            if dialog.is_group or dialog.is_channel:
                c=c+1
                group = dialog.entity
                print(dialog.title, group.id, group.username if hasattr(group,'username') else '' )
                if c>300:
                    exit()
                try:
                    supabase.table('sources').insert(
                        {"id":group.id, "profile": group.username if hasattr(group,'username') else group.id, "description": dialog.title, "platform": "telega",
                         "category": "todefine", "id_on_platform": group.id}).execute()
                except:
                    print('maybe exists')

                # dialog.entity: 'access_hash', 'admin_rights', 'banned_rights', 'broadcast', 'call_active', 'call_not_empty', 'creator', 'date', 'default_banned_rights', 'fake', 'forum', 'from_reader', 'gigagroup', 'has_geo', 'has_link', 'id', 'join_request', 'join_to_send', 'left', 'megagroup', 'min', 'noforwards', 'participants_count', 'photo', 'pretty_format', 'restricted', 'restriction_reason', 'scam', 'serialize_bytes', 'serialize_datetime', 'signatures', 'slowmode_enabled', 'stories_hidden', 'stories_hidden_min', 'stories_max_id', 'stories_unavailable', 'stringify', 'title', 'to_dict', 'to_json', 'username', 'usernames', 'verified']
                
                # dialog - 'archive', 'archived', 'date', 'delete', 'dialog', 'draft', 'entity', 'folder_id', 'id',
                #      'input_entity', 'is_channel', 'is_group', 'is_user', 'message', 'name', 'pinned', 'send_message', 'stringify',
                #      'title', 'to_dict', 'unread_count', 'unread_mentions_count']

def collect_posts(category="danceparty"):
    current_date =(datetime.date.today())
    kyivdancesources = supabase.table('sources').select("id, slug, topic, city").eq('media', 'telega').eq('category',category).limit(20).execute().data
    for source in kyivdancesources:
        print(source['slug'])

        if source['topic']:
            messages = parse_topic('vilyashko', source['slug'], source['topic'], 20)
        else:
            messages = parse_channel('vilyashko', source['slug'], 10)


        for message in messages:
            if message.text:
                #print(dir(message)); exit()
                text = (message.message).replace("\n", ". ")
                #text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
                post_date= (message.date).date()
                #print(message.date, current_date - post_date, message.text[:25])
                if (current_date - post_date).days>5:
                    break
                #, datetime.datetime.strptime(message.date, "%Y-%m-%d").date().days,
                post_to_save = {"fulltext": text, "source_slug": source['slug'], "category": category, "created_at": str(message.date),"city":source['city'], 'status': 'notreviewed', "post_id": message.id}
                print(text)
                try:
                    supabase.table('posts').insert(post_to_save).execute()
                except Exception as e:
                    print(str(e))
                    break



if __name__ == "__main__":
    collect_posts("dance")

def test():
    rez = parse_channel('alxwebdev', '', 20)  # 1442754450
    for message in rez:
        if message.text and not findPost(message.text, str(message.date)):
            addPost(message.text, str(message.date))
            print(message.date, message.chat_id, message.id, message.text[:15])

    rez = parse_topic('alxwebdev', 1373317798, 68773, 2)
    for message in rez:
        if message.text and not findPost(message.text, str(message.date)):
            addPost(message.text, str(message.date))
            print(message.date, message.chat_id, message.id, message.text[:15])


kyivdancesources = [{'descr':'social prime', 'group': 'https://t.me/kievsocialprime'}, {'descr':'costa rica', 'group':'https://t.me/KyivLatin', 'topic':62400}, {'descr':'Latin party in Kyiv', 'group':'https://t.me/latinpartyinkyiv'},{'descr':'Brazilian Zouk - Kyiv Events','group':'https://t.me/zouk_events_kyiv'}, {'descr':'Lago Family NEWS', 'group':'https://t.me/LagoFamilyNews'}] # , {'descr':'KIZOMBA social room', 'group':1400877269} , {'descr':'KSDC Chat','group':'https://t.me/KSDX_Chat'},

dnipro = [{'descr':'dnipro latin', 'group':'https://t.me/LatinPartyInDnipro'}]
odessa = [{'descr':'odessa latin','group':'https://t.me/LatinPartyInOdessa'},{'descr':'khazin odessa studio','group':'https://t.me/alex_khazin_salsa_studio'}]
lviv = [{'descr':'lviv main','group':'https://t.me/socialdanceinLviv'},{'descr':'Bachata Dance School Lviv UA',"group":'https://t.me/bdslviv'},{'decr':'lviv travel','group':'https://t.me/bdsl_events'},{'descr':'LA SALSA Lviv','group':'https://t.me/lasalsalviv'}]

# user group attributes
#     ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
#      '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__',
#      '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
#      '__weakref__', '_client', 'archive', 'archived', 'date', 'delete', 'dialog', 'draft', 'entity', 'folder_id', 'id',
#      'input_entity', 'is_channel', 'is_group', 'is_user', 'message', 'name', 'pinned', 'send_message', 'stringify',
#      'title', 'to_dict', 'unread_count', 'unread_mentions_count']

    # def sync_send(session: str, id, message: str):
    #     with tcsync(session, api_id, api_hash) as client:
    #         # print(id, message)
    #         client.send_message(id, message)
    #sync_send('alxwebdev', '@helvetian',"добрий день, а вакансія java-розробника ще актуальна? ")   #  581589257   629959045

