from flask import Flask, render_template
import pandas as pd
import os
import json
from collections import Counter
import csv
import re
from collections import defaultdict
    
app = Flask(__name__)

def find_most_mentioned_person(chat_file_path):
    # Regular expression pattern to detect mentions
    # Updated to include underscores and numbers which are common in usernames
    mention_pattern = re.compile(r'(?<!\w)@([a-zA-Z0-9_]{1,})')
    
    # Dictionary to store the mention count for each mentioned user
    mentioned_users_count = defaultdict(int)
    
    try:
        # Process each message in the chat.jsonl file
        with open(chat_file_path, "r", encoding="utf-8") as chat_file:
            for line_number, line in enumerate(chat_file, 1):
                try:
                    # Parse JSON line
                    data = json.loads(line)
                    message = data.get("message", "")
                    
                    # Find all mentions in the message
                    mentions = mention_pattern.findall(message)
                    
                    # Count each mention
                    for mentioned_user in mentions:
                        mentioned_users_count[mentioned_user.lower()] += 1
                    
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON on line {line_number}: {e}")
                    continue
                except Exception as e:
                    print(f"Error processing line {line_number}: {e}")
                    continue
        
        if not mentioned_users_count:
            return None, 0
        
        # Sort the users by the number of times they were mentioned (in descending order)
        sorted_mentions = sorted(mentioned_users_count.items(), 
                               key=lambda x: (x[1], x[0]), 
                               reverse=True)
        
        # Get the most mentioned person and their mention count
        most_mentioned_person = sorted_mentions[0][0]
        mention_count = sorted_mentions[0][1]
        
        # Print full statistics
        print("\nMention Statistics:")
        for user, count in sorted_mentions:
            print(f"@{user}: mentioned {count} times")
            
        return most_mentioned_person, mention_count
        
    except FileNotFoundError:
        print(f"Error: Chat file not found at {chat_file_path}")
        return None, 0
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return None, 0

def find_person_with_most_unique_mentions(chat_file_path):
    # Regular expression pattern to detect mentions
    mention_pattern = re.compile(r'(?<!\w)@([a-zA-Z0-9_]{1,})')
    
    # Dictionary to store the set of unique users mentioned by each person
    user_unique_mentions = defaultdict(set)
    
    try:
        # Process each message in the chat.jsonl file
        with open(chat_file_path, "r", encoding="utf-8") as chat_file:
            for line_number, line in enumerate(chat_file, 1):
                try:
                    # Parse JSON line
                    data = json.loads(line)
                    username = data.get("username", "").lower()
                    message = data.get("message", "")
                    
                    # Find all mentions in the message
                    mentions = mention_pattern.findall(message)
                    
                    # Add mentioned users to the set for this username
                    for mentioned_user in mentions:
                        # Don't count if someone mentions themselves
                        if mentioned_user.lower() != username:
                            user_unique_mentions[username].add(mentioned_user.lower())
                    
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON on line {line_number}: {e}")
                    continue
                except Exception as e:
                    print(f"Error processing line {line_number}: {e}")
                    continue
        
        if not user_unique_mentions:
            return None, 0, None
        
        # Convert sets to lengths and sort users by number of unique mentions
        unique_mention_counts = {
            username: len(mentions) 
            for username, mentions in user_unique_mentions.items()
        }
        
        sorted_users = sorted(
            unique_mention_counts.items(),
            key=lambda x: (x[1], x[0]),  # Sort by count first, then username
            reverse=True
        )
        
        # Get the user who mentioned the most unique people
        top_user = sorted_users[0][0]
        unique_count = sorted_users[0][1]
        mentioned_users = sorted(user_unique_mentions[top_user])  # Sort for consistent output
        
        # Print statistics
        print("\nUnique Mention Statistics:")
        for username, count in sorted_users:
            if count > 0:  # Only show users who mentioned others
                print(f"{username}: mentioned {count} unique users")
                print(f"  Mentioned: @{', @'.join(sorted(user_unique_mentions[username]))}")
        
        return top_user, unique_count, mentioned_users
        
    except FileNotFoundError:
        print(f"Error: Chat file not found at {chat_file_path}")
        return None, 0, None
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return None, 0, None

def get_newest_chat_file(chat_file_folder: str):
    chat_files = os.listdir(chat_file_folder)
    chat_files = [file for file in chat_files if file.endswith(".jsonl")]
    
    if not chat_files:
        return None
    
    newest_chat_file = max(chat_files, key=lambda x: os.path.getmtime(os.path.join(chat_file_folder, x)))
    return os.path.join(chat_file_folder, newest_chat_file)


@app.route('/')
def outro():

    chat_file_folder = "data"
    chat_file_path = get_newest_chat_file(chat_file_folder)
    emotes_file_path = "data/emotes.csv"
    emotes_default_file_path = "data/emotes_default.csv"

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
    
    most_mentioned, count = find_most_mentioned_person(chat_file_path)
    
    if most_mentioned:
        print(f"\nMost mentioned person: @{most_mentioned}")
        print(f"Times mentioned: {count}")
    else:
        print("No mentions found in the chat log.")

    top_mentioner, unique_count, mentioned_users = find_person_with_most_unique_mentions(chat_file_path)
        
    if top_mentioner:
        print(f"\nUser who mentioned the most unique people: {top_mentioner}")
        print(f"Number of unique people mentioned: {unique_count}")
        print(f"Users they mentioned: @{', @'.join(mentioned_users)}")
    else:
        print("No mentions found in the chat log.")

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

    return render_template('index.html', top_chatters=top_chatters, top_emotes=top_emotes, subscirber_amount=0,
                           chatters_amount=chatters_amount, new_chatters_amount=new_chatters_amount,
                           message_amount=message_amount, unique_emote_amount=unique_emote_amount, emote_amount=emote_amount, 
                           person_who_mentioned_most_unique_people = top_mentioner, person_who_typed_the_most_emotes=person_who_typed_the_most_emotes,
                           chatters=chatters, follower_amount=0, person_who_was_mentioned_the_most_times = most_mentioned)


if __name__ == '__main__':
    app.run(debug=True)
