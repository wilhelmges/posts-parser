import { ChatGPTAPI } from 'chatgpt'
import * as dotenv from 'dotenv'; dotenv.config();

const api = new ChatGPTAPI({
    apiKey: process.env.OPENAPI
})

const postNotEvent = `Розклад занять на 14.01 в Школі танців “SalsaBO”
📍SALSABO В ЦЕНТРІ

📍ВЕЛИКА ЖИТОМИРСЬКА, 24Б
❄️ 18:30
ЗАЛ 2: SALSA+BACHATA BEGINNERS NEW
Рівень: для початківців, з нуля
Викладач: Катя @kate_pustovit

❄️ 19:00
ЗАЛ 1: KIZOMBA INTERMEDIATE
Рівень: для тих, хто вже танцює
Викладачі: БОгдан і Таня

❄️ 20:00
ЗАЛ 2: SALSA + BACHATA INTERMEDIATE
Рівень: для тих, хто вже танцює
Викладачі: БО і Таня

📍ОЛІМПІЙСЬКА (Антоновича, 38а)

❄️ 19:00
ЗАЛ 2: URBAN KIZ INTERMEDIATE
Рівень: для тих, хто вже танцює
Вчителі: Іоанн та Настя @_angel_a_s_ @_ioann_el_hosri_

❄️ 19:00
ЗАЛ 2: URBAN KIZ BEGINNERS
Рівень: початковий
Вчитель: Артем

❄️ 20:00 СТАРТ КУРСА 🥁URBAN KIZ СТАЙЛИНГ В ПАРЕ
Рівень: для тих, хто вже танцює
Вчителі: Іоанн та Настя @_angel_a_s_ @_ioann_el_hosri_
_______________________________________________
Почни танцювати вже сьогодні з SALSABO!
ПОСТІЙНИЙ НАБІР В ГРУПИ ДЛЯ ПОЧАТКІВЦІВ! Всі, хто хоче навчитися танцювати Salsa, Bachata, Kizomba, Reggaeton пишіть в direct!
✔️Для запису в групи:
📲TEL. 097-410-06-51;
www.salsabo.com`
const postIsEvent = `Улюблена компанія, чудове місце зі світлом, кондиціонерами та зігріваючими напоями на барі, прекрасні діджеї, багато посмішок та танців - і ідеальний недільний вечір гарантовано 😍

🪩 3 великих зали на кожен стиль:
* БАЧАТА
🎧 качає Dj Shah
* ЗУК
🎧 запалює Dj Unizavr
* САЛЬСА
🎧 грає Dj Sanchez

📆 Коли: 12.01 (неділя) 19:00-22:00
📍 Де: Nivki Hall, проспект Берестейський, 84
💰Вхід: 250грн`

if (import.meta.url === `file://${process.argv[1]}`) {
    console.log(await calculateTextAnAnnouncementPossibility(postIsEvent))
}

export default async function calculateTextAnAnnouncementPossibility(text){
    const prompt = 'переглянь публікацію і розрахуй числову вірогідність того, що ця публікація є анонсом офлайн події. вкажи вірогідність як результат. вірогідність має бути виражена від 0 до 100. включи у відповідь виключно цифри, нічого зайвого. не треба пояснень, лише числове значення :'+text
    const res = await api.sendMessage(prompt)
    return Math.round(+res.text)
}

async function example() {
    const res = await api.sendMessage('яка мова використовується при розробці на платформі android? ')
    console.log(res.text)
}