from quart import Quart, request
from telegram import Bot

text="""
На сцені музика лунає,
Танок вогонь у серці має.
Ноги летять, як крила в птаха,
Ритм захоплює, душа не стиха.
"""
app = Quart(__name__)
bot = Bot(token="5602757659:AAGO_vOvgfb3p_EwEvNlky4QbeBLNA4oyVo")

async def send_message(chat_id, text):

    await bot.send_message(chat_id=chat_id, text=text)

@app.route('/send-message', methods=['GET'])
async def send_message_route():
    await bot.send_message(chat_id="@opendance_life",text=text, message_thread_id = 71477)
    return {"status": "success"}

if __name__ == "__main__":
    app.run(debug=True)
