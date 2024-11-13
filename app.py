from flask import Flask, render_template
import pandas as pd
import os
import json
from collections import Counter
import csv
import re
from collections import defaultdict
    
app = Flask(__name__)

# File paths
data_folder = r"C:\Users\zabit\Documents\GitHub\stream-outro\data"
emotes_file = os.path.join(data_folder, "emotes.csv")
emotes_default_file = os.path.join(data_folder, "emotes_default.csv")
top_chatters_file = os.path.join(data_folder, "top_chatters.csv")
top_emotes_file = os.path.join(data_folder, "top_emotes.csv")

@app.route('/')
def outro():
    # Path to the file
    file_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\subscribers_needed.txt"

    # Read the number from the file
    with open(file_path, "r", encoding="utf-8") as file:
        subscirber_amount = int(file.read().strip())

    # Print the result
    # print("subscirber_amount =", subscirber_amount)

    # Path to the .jsonl file
    file_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\chat.jsonl"

    # Counter to count the number of messages per username
    username_counter = Counter()

    # Dictionary to store the first message timestamp for each user
    first_message_timestamps = {}

    # Read the .jsonl file and process each line
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line)
            username = data.get("username")
            timestamp = data.get("timestamp")
            
            # Count the messages per username
            if username:
                username_counter[username] += 1
                
                # Store the first message timestamp for each unique user
                if username not in first_message_timestamps:
                    first_message_timestamps[username] = timestamp

    # Format the top chatters as required
    top_chatters = [{"username": user, "message_amount": count} for user, count in username_counter.most_common(18)]

    # Format the first message timestamps for each unique user
    chatters = [{"timestamp": first_message_timestamps[user], "username": user} for user in first_message_timestamps]
    
    print(chatters)

    # Convert the counter to the desired format
    top_chatters = [{"username": user, "message_amount": count} for user, count in username_counter.most_common(18)]
    

    # Path to the .jsonl file
    file_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\chat.jsonl"

    # Set to keep track of unique chatters
    unique_chatters = set()

    # Counters for the total messages and first-time chatters
    message_count = 0
    new_chatters_count = 0

    # Read the .jsonl file and process each line
    with open(file_path, "r", encoding="utf-8") as file:
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

    # Paths to the files
    chat_file_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\chat.jsonl"
    emotes_file_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\emotes.csv"
    emotes_default_file_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\emotes_default.csv"

    # Set to store all unique emote names
    emote_names = set()

    # Load emotes from emotes.csv
    with open(emotes_file_path, "r", encoding="utf-8") as emotes_file:
        csv_reader = csv.DictReader(emotes_file)
        for row in csv_reader:
            emote_names.add(row["Emote"])

    # Load emotes from emotes_default.csv
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

    # Calculate the number of unique emotes used
    unique_emote_amount = len(unique_emotes_used)
    
    emote_amount = emote_count
    
    unique_emote_amount = unique_emote_amount
    
    # Paths to the files
    chat_file_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\chat.jsonl"
    emotes_file_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\emotes.csv"
    emotes_default_file_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\emotes_default.csv"

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
    
    # Path to the chat file
    chat_file_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\chat.jsonl"

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
            
            # Find all mentions in the message
            mentions = mention_pattern.findall(message)
            
            # Count the mentions for this user
            if mentions:
                # print(f"{username} mentioned: {mentions}")  # Debug: print the mentions
                pass
            user_mentions_count[username] += len(mentions)

    # Sort the users by the number of mentions (in descending order)
    sorted_mentions = sorted(user_mentions_count.items(), key=lambda x: x[1], reverse=True)

    # Print the top 10 mentioners
    top_10_mentioners = sorted_mentions[:10]

    # Display the top 10 mentioners
    # print("\nTop 10 mentioners:")
    # for idx, (username, mentions) in enumerate(top_10_mentioners, start=1):
    #     print(f"{idx}. {username}: {mentions} mentions")

    # Find the user who mentioned others the most times
    person_who_mentioned_others_the_most_times = sorted_mentions[0][0]

    # Print the final result
    # print(f'\nperson_who_mentioned_others_the_most_times = "{person_who_mentioned_others_the_most_times}"')

    # Paths to the files
    chat_file_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\chat.jsonl"
    emotes_file_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\emotes.csv"
    emotes_default_file_path = r"C:\Users\zabit\Documents\GitHub\stream-outro\data\emotes_default.csv"

    # Set to store all unique emote names
    emote_names = set()

    # Load emotes from emotes.csv
    with open(emotes_file_path, "r", encoding="utf-8") as emotes_file:
        csv_reader = csv.DictReader(emotes_file)
        for row in csv_reader:
            emote_names.add(row["Emote"])

    # Load emotes from emotes_default.csv
    with open(emotes_default_file_path, "r", encoding="utf-8") as emotes_default_file:
        csv_reader = csv.DictReader(emotes_default_file)
        for row in csv_reader:
            emote_names.add(row["Emote Name"])

    # Compile a regular expression pattern to match emotes
    emote_pattern = re.compile(r'\b(' + '|'.join(re.escape(emote) for emote in emote_names) + r')\b')

    # Dictionary to store each user's emote count
    user_emote_counts = defaultdict(int)

    # Process each message in the chat.jsonl file
    with open(chat_file_path, "r", encoding="utf-8") as chat_file:
        for line in chat_file:
            data = json.loads(line)
            username = data.get("username")
            message = data.get("message", "")
            
            # Find all emote occurrences in the message
            found_emotes = emote_pattern.findall(message)
            
            # Add the count of emotes found in the message to the user's total
            user_emote_counts[username] += len(found_emotes)

    # Find the user with the highest emote count
    person_who_typed_the_most_emotes = max(user_emote_counts, key=user_emote_counts.get)

    # Print the result
    # print("person_who_typed_the_most_emotes =", f'"{person_who_typed_the_most_emotes}"')

    
    # Pass data to template
    return render_template('index.html', top_chatters=top_chatters, top_emotes=top_emotes, subscirber_amount=subscirber_amount,
                           chatters_amount=chatters_amount, new_chatters_amount=new_chatters_amount,
                           message_amount=message_amount, unique_emote_amount=unique_emote_amount, emote_amount=emote_amount, 
                           person_who_mentioned_others_the_most_times=person_who_mentioned_others_the_most_times, person_who_typed_the_most_emotes=person_who_typed_the_most_emotes,
                           chatters=chatters)

if __name__ == '__main__':
    app.run(debug=True)
