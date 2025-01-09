from ensta import Host as InstaClient # current https://github.com/diezo/ensta # not used https://github.com/subzeroid/instagrapi
import datetime, time
from repository import supabase #, get_sources, findPost, addPost
from random import randint
import re as regulars
from post_processor import calculate_event_possibility

# account = 'younglionrasmus' ; password='Fgzpz3XGQ8ZKvh2'
# shimabukurocoder Publ1cPassw0rd
instaClient = InstaClient('younglionrasmus', 'Fgzpz3XGQ8ZKvh2')

def getposts(category='dance'):
    current_date = (datetime.date.today())
    sources = supabase.table('sources').select("id, slug, category").eq('media','insta').eq('category',category).execute().data
    for source in sources:  # host.followings(account, count=0):  # users we are watching. Want full list? Set count to '0'
        slug = source['slug']
        print(slug)
        try:
            posts = instaClient.posts(slug, 10)  # Want full list? Set count to '0'
        except(e):
            print('error, while getting posts', e, str(e), dir(e), type(e))
            continue
        first = True
        for post in posts:  # post <class 'ensta.containers.Post.Post'>
            if not hasattr(post, 'caption_text'):
                continue
            if supabase.table('posts').select("id").eq('post_id',post.post_id).eq('category',category).execute().data:
                if first:
                    pinned_space = True
                first = False
            pass
            text = post.caption_text.replace("\n", ". ")
            post_date = datetime.datetime.fromtimestamp(post.caption_created_at).date() # post.caption_created_at  1706391694, post.caption_created_at вроде соответсвует дате последнего редактирования
            if text:
                if (current_date - post_date).days>14:
                    break
                possibility = calculate_event_possibility(text)
                # print(post.post_id, post.code,post_date, text[:30]); exit()
                post_to_save = {"source_slug": slug, "fulltext": text, "category": category, "created_at": str(post_date), 'status':'notreviewed', "post_id":post.post_id,"url_slug": post.code, "possibility": possibility}
                try:
                    supabase.table('posts').insert(post_to_save).execute()
                except Exception as e:
                    print('maybe exist', e, str(e), dir(e), type(e))
                    continue
            time.sleep(randint(90,190))

        #supabase.table('sources').update({'scanned': str(current_date)}).eq('id', user['id']).execute() ;         time.sleep(randint(10,55))
        print('-------------')

def grab_insta_profile_lastposts(profile: str, limit=12): # sens_khreshchatyk
    posts = instaClient.posts(profile, limit)  # Want full list? Set count to '0'
    for post in posts:
        #print(post.post_id, post.code, )
        print(dir(post))
        if not hasattr(post, 'caption_text'):
            continue
        text =  post.caption_text.replace("\n", ". ")
        print(post.post_id, post.code, text[:50])

def iterate_insta_sources(category='culture'):
    # current_date = (datetime.date.today()) ; insta_client = InstaClient(account, password)
    sources = (supabase.table('sources').select("id, slug, category")
               .eq('media', 'insta').eq('category','church').execute().data)
    for item in sources:  # host.followings(account, count=0):  # users we are watching. Want full list? Set count to '0'
        slug = item['slug']
        grab_insta_profile_lastposts(slug, 3)

if __name__ == '__main__':
    pass
    getposts('tusa')

    #iterate_insta_sources('church')
    # grab_insta_profile_lastposts('alfa.church', instaClient, 3)

def grabb_sources():
    pass
    for user in host.followings(account, count=0):
        source = user.username
        print(user.full_name)
        #supabase.table('sources').insert({"profile": user.username, "description": user.full_name, "platform": "insta","category": "culture"}).execute()

def stamp_to_normal(stamp):
    return datetime.datetime.fromtimestamp(stamp)

def uplotest():
    msg = """
    Diverse Sources of Energy🌆 :
The world relies on a diverse array of energy sources to meet its growing demands. Traditional fossil fuels such as coal, oil, and natural gas have been the primary contributors to global energy consumption. However, these sources are finite, environmentally detrimental, and contribute to climate change. On the other hand, renewable energy sources, including solar, wind, hydropower, and geothermal, offer a cleaner and more sustainable alternative.
The Environmental Toll of Fossil Fuels:
Fossil fuel combustion releases greenhouse gases, such as carbon dioxide, into the atmosphere, leading to global warming and climate change. Moreover, the extraction and transportation of fossil fuels result in environmental degradation, habitat destruction, and oil spills, causing irreparable harm to ecosystems. The urgent need to reduce our reliance on these sources is evident to mitigate the adverse effects on the planet.
    """
    upload = host.get_upload_id("sundaytest.jpg")
    host.upload_photo(upload, caption=msg)

# for attr in dir(post):
#     if not attr.startswith("__"):
#         print(f"{attr}: {getattr(post, attr)}")
# post.post_id
# print( post.caption_text, file=f); print('-------------', file=f) #post.post_id
