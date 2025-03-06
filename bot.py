from pyrofork import Client, filters
from decouple import config
import logging
import asyncio
import uvloop

# Install uvloop for better performance on Unix systems
uvloop.install()

# Configure logging
logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING
)

print("Starting...")

# Load configuration using python-decouple
APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION")

# Source chat IDs to monitor
FROM = [-1001391583159, -1001201589228, -1001288752850]

# Target bot username
TO_BOT_USERNAME = "@ExtraPeBot"

# Initialize the Pyrofork client
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

# Start the bot and keep it running
async def start_bot():
    await BotzHubUser.start()
    user = await BotzHubUser.get_me()
    print(f"Logged in as: {user.first_name}")

    # Keep the bot running indefinitely
    await asyncio.Event().wait()

# Handle messages from specified chats
@BotzHubUser.on_message(filters.chat(FROM))
async def sender_bH(client, message):
    try:
        # Copy the message to the target bot
        await client.copy_message(
            chat_id=TO_BOT_USERNAME,
            from_chat_id=message.chat.id,
            message_id=message.id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=message.reply_markup
        )
    except Exception as e:
        print(f"Error copying message: {e}")

# Run the bot
if __name__ == "__main__":
    BotzHubUser.run(start_bot())
