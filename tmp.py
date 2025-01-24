from telegram import Bot
import asyncio

# Initialize the bot with your token

text="""
На сцені музика лунає,
Танок вогонь у серці має.
Ноги летять, як крила в птаха,
Ритм захоплює, душа не стиха.
"""
bot = Bot(token="5602757659:AAGO_vOvgfb3p_EwEvNlky4QbeBLNA4oyVo")


# Chat ID of the group
chat_id = "@opendance_life" #-2073535024  # Replace with your group's chat ID

# ID of the topic (thread) within the group
message_thread_id = 71477  # Replace with the ID of the topic

# Send a message to the specific chat topic
async def main():
    await bot.send_message(
        chat_id=chat_id,text=text,
        message_thread_id=message_thread_id
    )

asyncio.run(main())