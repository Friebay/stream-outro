import requests
import csv
import os
from dotenv import load_dotenv

load_dotenv() # Load variables from .env file

client_id = os.getenv('TWITCH_CLIENT_ID')
access_token = os.getenv('TWITCH_ACCESS_TOKEN')

# Set up the headers for the API request
headers = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {access_token}'
}

# URL for fetching global emotes
url = "https://api.twitch.tv/helix/chat/emotes/global"

# Make the request to the Twitch API
response = requests.get(url, headers=headers)

if response.status_code == 200:
    emotes = response.json()['data']

    # Open the CSV file to write the data
    with open(r"data\emotes_default.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        
        # Write the header
        writer.writerow(['Emote Name', 'Image URL'])
        
        # Write the emote data
        for emote in emotes:
            emote_name = emote['name']
            emote_id = emote['id']
            emote_image_url = f"https://static-cdn.jtvnw.net/emoticons/v2/{emote_id}/default/dark/3.0"
            
            # Write each emote's name and image URL into the CSV
            writer.writerow([emote_name, emote_image_url])
            
    print("Emotes saved successfully to emotes_default.csv.")
else:
    print(f"Error: Unable to fetch emotes. Status code: {response.status_code}")
