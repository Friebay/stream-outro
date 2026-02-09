import requests
import csv

def get_emote_set_emotes(emote_set_id):
    url = f"https://7tv.io/v3/emote-sets/{emote_set_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        # Check if 'emotes' is in the response
        if 'emotes' in data:
            emotes = data['emotes']
            emote_names = [emote['name'] for emote in emotes]  # List of emote names
            emote_ids = [emote['id'] for emote in emotes]
            emote_image_url = [f"https://cdn.7tv.app/emote/{emote['id']}/1x.webp" for emote in emotes]
            return emote_names, emote_ids, emote_image_url
        else:
            print("No emotes found in this emote set.")
            return [], [], []
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return [], [], []

def save_emotes_to_csv(emote_set_id, filename="data/emotes.csv"):
    emotes, ids, emote_image_urls = get_emote_set_emotes(emote_set_id)
    
    if emotes and ids and emote_image_urls:
        with open(filename, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(["Emote", "ID", "Image URL"])  # Header row
            for emote, emote_id, url in zip(emotes, ids, emote_image_urls):
                writer.writerow([emote, emote_id, url])
        print(f"Emotes saved to {filename}")
    else:
        print("No data to save.")

# Example usage with the specified emote set ID
emote_set_id = "01HDXTX0F0000EW388NZZBSEYW"
save_emotes_to_csv(emote_set_id)
