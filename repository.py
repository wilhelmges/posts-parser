import hashlib, os
from datetime import datetime

import os
from supabase import create_client, Client

from dotenv import load_dotenv; load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def get_sources():
    response = supabase.table('sources').select("id, slug").eq('category','church').execute()
    return response.data

def findPost(text, date):
    sha256_hash = hashlib.sha256()
    encoded_string = (text+date).encode()
    sha256_hash.update(encoded_string)
    hex_digest = sha256_hash.hexdigest()
    cur.execute(f"SELECT * FROM raw_posts WHERE hash='{hex_digest}' LIMIT 1")
    rows = cur.fetchall()
    return bool(rows)

def addPost(text, date, source='unknown'):
    sql = '''INSERT INTO raw_posts(hash, text, category, created_at, source) VALUES(?,?,?,?,?)'''
    sha256_hash = hashlib.sha256()
    encoded_string = (text+date).encode()
    sha256_hash.update(encoded_string)
    hex_digest = sha256_hash.hexdigest()
    current_dateTime = datetime.now()
    cur.execute(sql, (hex_digest, text, 'unknown', date, source ))
    conn.commit()

if __name__ == '__main__':
    pass
    # print(get_sources())
    # print(findPost('hello, test 3'))
    # addRawPost('hello, test')
    #

    #  def test_turso():
    #     url = 'libsql://event-calendo-vetsinen.turso.io' # os.getenv("LIBSQL_URL")
    #     auth_token = 'eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyRmRoQ0w3Y0VlNm42ZktjdkNoMHJ3In0.9oakF2kZ3Wc-Um0ElNL2JKZkThYtbrK40QxWOugyP0sH8eUgtYJ5KfYv-GLBodvOvvPkM4hme4gK3nAkYBZYBw' #os.getenv("LIBSQL_AUTH_TOKEN")
    #
    #     con = libsql.connect(database=url, auth_token=auth_token)
    #     cur = con.cursor()