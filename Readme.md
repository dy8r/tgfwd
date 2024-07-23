
# Telegram Channel Forwarder Bot

This Telegram bot automates the forwarding of messages from specified Telegram channels into a specified Telegram topic. 

## Features

- Start and help commands for user guidance.
- Add and remove channels to/from the forward list.
- List all channels currently in the forward list.
- Automatically forward messages from the specified channels to a designated topic.

## Prerequisites

- Python 3.7 or higher
- Telegram account with a bot token

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required libraries using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `config.py` file in the root directory with the following content:
   ```python
   API_ID = 'your_api_id'
   API_HASH = 'your_api_hash'
   BOT_TOKEN = 'your_bot_token'
   CHAT_LINK = 'your_chat_link'
   ADMIN_IDS = [123456789, 987654321]  # List of Telegram user IDs who can manage the bot
   ```

## Running the Bot

1. Run the bot script:
   ```bash
   python bot.py
   ```

2. The bot will be up and running, ready to accept commands.

## Commands

- `/start` - Welcome message.
- `/help` - List of available commands.
- `/add_author <channel_link> <topic_id>` - Add a channel to the forward list.
- `/remove_author <channel_link>` - Remove a channel from the forward list.
- `/see_authors` - List all channels in the forward list.

## Example Usage

1. Start the bot by sending `/start`.
2. Get help by sending `/help`.
3. Add a channel to the forward list by sending `/add_author @example_channel 123`.
4. Remove a channel from the forward list by sending `/remove_author @example_channel`.
5. List all channels in the forward list by sending `/see_authors`.
