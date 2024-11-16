from flask import Flask, render_template
import pandas as pd
import os
import json
from collections import Counter
import csv
import re
from collections import defaultdict
    
app = Flask(__name__)

@app.route('/')
def outro():
    subscribers_needed_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\subscribers_needed.txt"

    with open(subscribers_needed_path, "r", encoding="utf-8") as file:
        subscirber_amount = int(file.read().strip())

    chat_file_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\chat.jsonl"
    emotes_file_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\emotes.csv"
    emotes_default_file_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\emotes_default.csv"

    username_counter = Counter()

    first_message_timestamps = {}

    with open(chat_file_path, "r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line)
            username = data.get("username")
            timestamp = data.get("timestamp")
            timestamp = timestamp.replace("T", " ")
            
            if username:
                username_counter[username] += 1
                
                # Store the first message timestamp for each unique user
                if username not in first_message_timestamps:
                    first_message_timestamps[username] = timestamp

    # Format the top chatters as required
    top_chatters = [{"username": user, "message_amount": count} for user, count in username_counter.most_common(18)]

    # Format the first message timestamps for each unique user
    chatters = [{"timestamp": first_message_timestamps[user], "username": user} for user in first_message_timestamps]

    # Convert the counter to the desired format
    top_chatters = [{"username": user, "message_amount": count} for user, count in username_counter.most_common(18)]

    # Set to keep track of unique chatters
    unique_chatters = set()

    message_count = 0
    new_chatters_count = 0

    with open(chat_file_path, "r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line)
            username = data.get("username")
            is_first_time_chatter = data.get("is_first_time_chatter", False)
            
            # Count each line as a message
            message_count += 1
            
            # Track unique chatters
            if username:
                unique_chatters.add(username)
            
            # Count first-time chatters
            if is_first_time_chatter:
                new_chatters_count += 1

    chatters_amount = len(unique_chatters)
    new_chatters_amount = new_chatters_count
    message_amount = message_count

    emote_names = set()

    with open(emotes_file_path, "r", encoding="utf-8") as emotes_file:
        csv_reader = csv.DictReader(emotes_file)
        for row in csv_reader:
            emote_names.add(row["Emote"])

    with open(emotes_default_file_path, "r", encoding="utf-8") as emotes_default_file:
        csv_reader = csv.DictReader(emotes_default_file)
        for row in csv_reader:
            emote_names.add(row["Emote Name"])

    # Compile a regular expression pattern to match emotes
    emote_pattern = re.compile(r'\b(' + '|'.join(re.escape(emote) for emote in emote_names) + r')\b')

    # Counter for total emote occurrences and a set to track unique emotes used
    emote_count = 0
    unique_emotes_used = set()

    # Process each message in the chat.jsonl file
    with open(chat_file_path, "r", encoding="utf-8") as chat_file:
        for line in chat_file:
            data = json.loads(line)
            message = data.get("message", "")
            
            # Find all emote occurrences in the message
            found_emotes = emote_pattern.findall(message)
            
            # Update the total emote count and track unique emotes
            emote_count += len(found_emotes)
            unique_emotes_used.update(found_emotes)

    unique_emote_amount = len(unique_emotes_used)
    
    emote_amount = emote_count
    
    unique_emote_amount = unique_emote_amount

    # Dictionary to store emote data (name -> {name, image link})
    emote_data = {}

    # Load emotes from emotes.csv
    with open(emotes_file_path, "r", encoding="utf-8") as emotes_file:
        csv_reader = csv.DictReader(emotes_file)
        for row in csv_reader:
            emote_data[row["Emote"]] = {
                "name": row["Emote"],
                "webp": row["Image URL"]
            }

    # Load emotes from emotes_default.csv
    with open(emotes_default_file_path, "r", encoding="utf-8") as emotes_default_file:
        csv_reader = csv.DictReader(emotes_default_file)
        for row in csv_reader:
            emote_data[row["Emote Name"]] = {
                "name": row["Emote Name"],
                "webp": row["Image URL"]
            }

    # Compile a regular expression pattern to match emotes
    emote_pattern = re.compile(r'\b(' + '|'.join(re.escape(emote) for emote in emote_data.keys()) + r')\b')

    # Counter for emote occurrences
    emote_counter = Counter()

    # Process each message in the chat.jsonl file
    with open(chat_file_path, "r", encoding="utf-8") as chat_file:
        for line in chat_file:
            data = json.loads(line)
            message = data.get("message", "")
            
            # Find all emotes in the message and update their counts
            found_emotes = emote_pattern.findall(message)
            emote_counter.update(found_emotes)

    # Extract the top 18 most popular emotes with their information
    top_emotes = [
        {
            "webp": emote_data[emote]["webp"],
            "name": emote_data[emote]["name"],
            "amount": count
        }
        for emote, count in emote_counter.most_common(18)
    ]

    # Regular expression pattern to detect mentions
    mention_pattern = re.compile(r'(?<!\w)@([a-zA-Z]{3,})')

    # Dictionary to store the mention count for each user
    user_mentions_count = defaultdict(int)

    # Process each message in the chat.jsonl file
    with open(chat_file_path, "r", encoding="utf-8") as chat_file:
        for line in chat_file:
            data = json.loads(line)
            username = data.get("username")
            message = data.get("message", "")
            
            mentions = mention_pattern.findall(message)
            
            if mentions:
                pass
            user_mentions_count[username] += len(mentions)

    # Sort the users by the number of mentions (in descending order)
    sorted_mentions = sorted(user_mentions_count.items(), key=lambda x: x[1], reverse=True)

    # Find the user who mentioned others the most times
    person_who_mentioned_others_the_most_times = sorted_mentions[0][0]

    emote_names = set()

    with open(emotes_file_path, "r", encoding="utf-8") as emotes_file:
        csv_reader = csv.DictReader(emotes_file)
        for row in csv_reader:
            emote_names.add(row["Emote"])

    with open(emotes_default_file_path, "r", encoding="utf-8") as emotes_default_file:
        csv_reader = csv.DictReader(emotes_default_file)
        for row in csv_reader:
            emote_names.add(row["Emote Name"])

    emote_pattern = re.compile(r'\b(' + '|'.join(re.escape(emote) for emote in emote_names) + r')\b')

    user_emote_counts = defaultdict(int)

    with open(chat_file_path, "r", encoding="utf-8") as chat_file:
        for line in chat_file:
            data = json.loads(line)
            username = data.get("username")
            message = data.get("message", "")
            
            found_emotes = emote_pattern.findall(message)
            
            user_emote_counts[username] += len(found_emotes)

    person_who_typed_the_most_emotes = max(user_emote_counts, key=user_emote_counts.get)

    return render_template('index.html', top_chatters=top_chatters, top_emotes=top_emotes, subscirber_amount=subscirber_amount,
                           chatters_amount=chatters_amount, new_chatters_amount=new_chatters_amount,
                           message_amount=message_amount, unique_emote_amount=unique_emote_amount, emote_amount=emote_amount, 
                           person_who_mentioned_others_the_most_times=person_who_mentioned_others_the_most_times, person_who_typed_the_most_emotes=person_who_typed_the_most_emotes,
                           chatters=chatters)


if __name__ == '__main__':
    app.run(debug=True)
