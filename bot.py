from pyrogram import Client, filters
from decouple import config
import logging
import asyncio
import uvloop

uvloop.install()

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

print("Starting...")

APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION")

FROM = [-1001391583159, -1001201589228, -1001288752850]
TO_BOT_USERNAME = "@ExtraPeBot"

try:
    BotzHubUser = Client(
        name="BotzHubUser",
        api_id=APP_ID,
        api_hash=API_HASH,
        session_string=SESSION
    )
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)

async def start_bot():
    await BotzHubUser.start()
    user = await BotzHubUser.get_me()
    print(f"Logged in as: {user.first_name}")
    await asyncio.Event().wait()  # Keeps the bot running indefinitely

@BotzHubUser.on_message(filters.chat(FROM))
async def sender_bH(client, message):
    try:
        await client.copy_message(
            chat_id=TO_BOT_USERNAME,
            from_chat_id=message.chat.id,
            message_id=message.id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=message.reply_markup
        )
    except Exception as e:
        print(f"Error forwarding message: {e}")

# Properly run the bot
if __name__ == "__main__":
    asyncio.run(BotzHubUser.run(start_bot))
