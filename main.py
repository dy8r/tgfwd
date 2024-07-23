import json
import os
from telethon import TelegramClient, events, functions, types
from config import API_ID, API_HASH, BOT_TOKEN, CHAT_LINK, ADMIN_IDS

# Define the file path for the database
DB_FILE = 'db.json'

# Initialize an empty dictionary to store channel-topic mappings
channel_topic_map = {}

# Load or initialize the database
if not os.path.exists(DB_FILE):
    # If the database file does not exist, create an empty JSON file
    with open(DB_FILE, 'w') as db_file:
        json.dump({}, db_file)
else:
    # If the database file exists, load the channel-topic mappings
    with open(DB_FILE, 'r') as db_file:
        channel_topic_map = json.load(db_file)

# Create the Telegram client and connect to the API
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Define the /start command handler
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(
        "Welcome to the Channel Forwarder Bot!\n"
        "Use /help to see available commands."
    )

# Define the /help command handler
@client.on(events.NewMessage(pattern='/help'))
async def help(event):
    await event.respond(
        "Available commands:\n"
        "/add_author <channel_link> <topic_id> - Add a channel to the forward list.\n"
        "/remove_author <channel_link> - Remove a channel from the forward list.\n"
        "/see_authors - List all channels in the forward list."
    )

# Define the /add_author command handler
@client.on(events.NewMessage(pattern='/add_author'))
async def add_author(event):
    # Check if the sender is an admin
    if event.sender_id in ADMIN_IDS:
        parts = event.raw_text.split()
        if len(parts) == 3:
            channel_link, topic_id = parts[1], parts[2]
            # Normalize the channel link format
            if channel_link.startswith('https://t.me/'):
                channel_link = channel_link[13:]
            if channel_link.startswith('@'):
                channel_link = channel_link[1:]
            # Update the channel-topic mapping and save to the database
            channel_topic_map[channel_link] = topic_id
            with open(DB_FILE, 'w') as db_file:
                json.dump(channel_topic_map, db_file)
            await event.respond(f'Author added: {channel_link} -> {topic_id}')
        else:
            await event.respond('Usage: /add_author channel_link topic_id. \n\nChannel link should be in one of the following formats: \n@channel \nhttps://t.me/channel \nchannel')
    else:
        await event.respond('Unauthorized')

# Define the /remove_author command handler
@client.on(events.NewMessage(pattern='/remove_author'))
async def remove_author(event):
    # Check if the sender is an admin
    if event.sender_id in ADMIN_IDS:
        parts = event.raw_text.split()
        if len(parts) == 2:
            channel_link = parts[1]
            # Remove the channel from the database if it exists
            if channel_link in channel_topic_map:
                del channel_topic_map[channel_link]
                with open(DB_FILE, 'w') as db_file:
                    json.dump(channel_topic_map, db_file)
                await event.respond(f'Author removed: {channel_link}')
            else:
                await event.respond('Channel link not found in database')
        else:
            await event.respond('Usage: /remove_author channel_link')
    else:
        await event.respond('Unauthorized')

# Define the /see_authors command handler
@client.on(events.NewMessage(pattern='/see_authors'))
async def see_authors(event):
    # Check if the sender is an admin
    if event.sender_id in ADMIN_IDS:
        if channel_topic_map:
            # Respond with the list of current authors
            response = 'Current authors:\n' + '\n'.join([f'{k} -> {v}' for k, v in channel_topic_map.items()])
            await event.respond(response)
        else:
            await event.respond('No authors found')
    else:
        await event.respond('Unauthorized')

# Define a handler for all new messages
@client.on(events.NewMessage)
async def handler(event):
    try:
        # Get the channel username from the event
        channel_link = event.chat.username
        print(channel_link)
        # Check if the channel is in the channel-topic map
        if channel_link in channel_topic_map:
            topic_id = channel_topic_map[channel_link]
            # Forward the message to the specified chat and topic
            await client(functions.messages.ForwardMessagesRequest(
                from_peer=channel_link,
                id=[event.message.id],
                to_peer=CHAT_LINK,
                top_msg_id=int(topic_id)
            ))
            print(f'Message forwarded: {event.message.text}')
            # Notify all admins about the forwarded message
            for admin_id in ADMIN_IDS:
                await client.send_message(admin_id, f'Message forwarded: {event.message.text}')
    except Exception as e:
        # Print any errors that occur during message forwarding
        print(f'Error forwarding message: {e}')

# Print a message indicating that the bot is running
print("Bot is running...")
# Run the client until disconnected
client.run_until_disconnected()
