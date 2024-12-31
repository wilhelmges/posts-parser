import locale
import time
locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')

date_str = time.strftime("%A - %d %B")
print(date_str)

exit()

from datetime import datetime

date_string = "2024.18.02"
formatted_date = datetime.strptime(date_string, "%Y.%d.%m").date()

print(formatted_date)

exit()
def coher():
    co = cohere.Client('1OeBh5wDs3BZZQUCFPFnrZyIvOi4BHDVaNAzoi2p')
    text = '''
    у Києві презентуємо книжку Максима Паламарчука «Бойові кораблі. Еволюція лінкорів та авіаносців».

👤Максим — керівник центру зовнішньополітичних досліджень у Національному інституті стратегічних досліджень. Працював в Апараті РНБО України. 

📖У цій книжці він описує еволюцію основних бойових кораблів у стратегічному середовищі, як результат взаємодії численних різноспрямованих впливів: політики, технологій, державних бюджетів, поглядів адміралів на тактику застосування флоту і, не в останню чергу, закономірностей та випадковостей війни. 

👤Модеруватиме розмову Катерина Супрун, авторка проєктів на «Мілітарному». 

•  Коли? 7 лютого о 19:00 
•  Де? Книгарня «Є» на вул. Лисенка, 3 
•  Вхід вільний 
Книжку можна буде придбати у книгарні під час презентації.

    '''
    prediction = co.chat(message='надай коротку відповідь українською, у відповіді вкажи дату проведення у форматі json, без зайвої інформації: '+text, model='command')
    print(f'Chatbot: {prediction.text}')


# print(type(chat_completion)) ; print(dir(chat_completion)) ; print(chat_completion)
rez = response.choices[0].message.content
print(rez)
exit()
import datetime
date1 = datetime.date(2023, 12, 31)
date2 = datetime.date(2023, 1, 1)

print(type(date1), type(date2))
# Calculate the difference in days
difference_in_days = (date1 - date2).days

# print("Difference in days:", difference_in_days)


exit()
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('strapi-dashboard/.tmp/data.db')

# Create a cursor object
cur = conn.cursor()

# Execute a SELECT statement
cur.execute("SELECT * FROM categories LIMIT 1")
rows = cur.fetchall()

# Print all the rows
for row in rows:
    print(row)

# Close the connection
conn.close()
