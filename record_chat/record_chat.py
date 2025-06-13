import twitchio
from twitchio.ext import commands
import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv() # Load variables from .env file

# Define the save directory
SAVE_DIR = r"data"

# Load credentials and configuration from .env file
BOT_TOKEN = os.getenv('TWITCH_ACCESS_TOKEN')
BOT_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')

channel_to_record = 'thexanos'

if not BOT_TOKEN:
    raise ValueError("TWITCH_ACCESS_TOKEN not found in .env file. Please add it.")
if not BOT_CLIENT_ID:
    raise ValueError("TWITCH_CLIENT_ID not found in .env file. Please add it.")

class TwitchChatBot(commands.Bot):
    def __init__(self):
        # Initialize with your credentials
        super().__init__(
            token=BOT_TOKEN,
            client_id=BOT_CLIENT_ID,
            nick=channel_to_record,
            prefix='!',
            initial_channels=[channel_to_record]
        )
        self.log_file: str | None = None # Added type hint
        
        # Create directory if it doesn't exist
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
            print(f"Created directory: {SAVE_DIR}")
        
    async def event_ready(self):
        print(f'Bot is ready | Logged in as {self.nick}')
        # Create a new log file with timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = os.path.join(SAVE_DIR, f'thexanos_chat_log_{timestamp}.jsonl')
        print(f'Logging chat to: {self.log_file}')
        print('Monitoring thexanos\'s chat...')

    async def event_message(self, message: twitchio.Message): # Added type hint for message
        # Skip messages from the bot itself
        if message.echo:
            return

        if not self.log_file: # Check if log_file is initialized
            print("Error: Log file not initialized. Skipping message logging.")
            return
            
        # Check if first-time chatter using tags
        is_first_time = message.tags.get('first-msg', '0') == '1'
            
        # Create message data structure
        chat_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'username': message.author.name,
            'message': message.content,
            'is_subscriber': message.author.is_subscriber,
            'is_mod': message.author.is_mod,
            'is_first_time_chatter': is_first_time,
            'badges': message.author.badges,
            'color': message.author.color
        }
        
        try:
            # Save to file with ensure_ascii=False for proper Lithuanian character encoding
            with open(self.log_file, 'a', encoding='utf-8') as f:
                json.dump(chat_data, f, ensure_ascii=False, default=str)
                f.write('\n')
                
            # Print to console with first-time chatter indicator
            first_time_indicator = "🆕 " if is_first_time else ""
            print(f'[{chat_data["timestamp"]}] {first_time_indicator}{chat_data["username"]}: {chat_data["message"]}')
            
            # Special console message for first-time chatters
            if is_first_time:
                print(f'>>> First-time chatter detected: {message.author.name} <<<')
                
        except Exception as e:
            print(f"Error saving message: {e}")

def main():
    try:
        bot = TwitchChatBot()
        print('Starting bot...')
        print(f'Chat logs will be saved to: {SAVE_DIR}')
        print('🆕 symbol indicates first-time chatters')
        bot.run()
    except Exception as e:
        print(f"Error running bot: {e}")

if __name__ == '__main__':
    main()