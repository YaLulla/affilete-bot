from pyrogram import Client, filters
from decouple import config
import logging
import asyncio
import uvloop

# Install uvloop for faster event loop handling
uvloop.install()

# Set up logging for debug or production purposes
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

print("Starting...")

# Load environment variables
APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION")

# Source chats to listen to and target bot username
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
except Exception as e:
    print(f"ERROR - {e}")
    exit(1)

@BotzHubUser.on_message(filters.chat(FROM))
async def sender_bH(client, message):
    """
    Handler to forward messages from specified chats to a bot.
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
    Main entry point for the bot.
    Starts the client and manages the event loop.
    """
    async with BotzHubUser:
        user = await BotzHubUser.get_me()
        print(f"Logged in as: {user.first_name}")
        # Keep the bot running
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
