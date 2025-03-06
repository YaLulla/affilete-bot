from pyrogram import Client, filters
from decouple import config
import logging
import asyncio
import uvloop

# Install uvloop for improved event loop performance
uvloop.install()

# Configure logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

print("Starting...")

# Load configuration variables
APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION")

# Chat IDs to forward messages from and bot username to forward to
FROM = [-1001391583159, -1001201589228, -1001288752850]
TO_BOT_USERNAME = "@ExtraPeBot"

# Initialize the bot client
try:
    BotzHubUser = Client(
        name=SESSION,
        api_id=APP_ID,
        api_hash=API_HASH,
        session_string=SESSION
    )
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)

@BotzHubUser.on_message(filters.chat(FROM))
async def sender_bH(client, message):
    """
    Forward messages from specified chats to the target bot.
    """
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
        print(f"Error while forwarding message: {e}")

async def main():
    """
    Start the bot and handle the event loop properly.
    """
    async with BotzHubUser:
        user = await BotzHubUser.get_me()
        print(f"Logged in as: {user.first_name}")
        # Keep the bot running until interrupted
        await asyncio.Event().wait()

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
