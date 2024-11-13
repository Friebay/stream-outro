from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

# File paths
data_folder = r"C:\Users\zabit\Documents\GitHub\stream-outro\data"
emotes_file = os.path.join(data_folder, "emotes.csv")
emotes_default_file = os.path.join(data_folder, "emotes_default.csv")
top_chatters_file = os.path.join(data_folder, "top_chatters.csv")
top_emotes_file = os.path.join(data_folder, "top_emotes.csv")

@app.route('/')
def outro():
    # Load CSV files
    emotes = pd.read_csv(emotes_file)
    emotes_default = pd.read_csv(emotes_default_file)
    top_chatters = pd.read_csv(top_chatters_file)
    top_emotes = pd.read_csv(top_emotes_file)
    
    subscirber_amount = 56000

    # Convert data to dictionaries for easy template rendering
    emotes = emotes.to_dict(orient='records')
    emotes_default = emotes_default.to_dict(orient='records')
    top_chatters = [
        {"username": "User1", "message_amount": 120},
        {"username": "User2", "message_amount": 105},
        {"username": "User1", "message_amount": 100},
        {"username": "User2", "message_amount": 96},
        {"username": "User1", "message_amount": 80},
        {"username": "User2", "message_amount": 70},
        {"username": "User1", "message_amount": 60},
        {"username": "User2", "message_amount": 20},
        {"username": "User1", "message_amount": 10},
        {"username": "User2", "message_amount": 1}
    ]
    top_emotes = [
        {"webp": "https://static-cdn.jtvnw.net/emoticons/v2/555555560/default/dark/3.0", "name": ":D", "amount": 281},
        {"webp": "https://static-cdn.jtvnw.net/emoticons/v2/425618/default/dark/3.0", "name": "LUL", "amount": 69},
        {"webp": "https://cdn.7tv.app/emote/01GR7R0H9G000FEKDNHQTECH62/4x.webp", "name": "kur", "amount": 42},
        {"webp": "https://static-cdn.jtvnw.net/emoticons/v2/25/default/dark/3.0", "name": "Kappa", "amount": 37},
        {"webp": "https://cdn.7tv.app/emote/01FF3R5C30000FF5VVCKV49G6J/4x.webp", "name": "xdd", "amount": 22}
    ]
    
    chatters = [
        {"timestamp": "2024-11-10T20:26:22.062497", "username": "friebay"},
        {"timestamp": "2024-11-10T20:30:13.260583", "username": "domminnique"},
        {"timestamp": "2024-11-10T20:30:34.164366", "username": "karolinskiss"},
        {"timestamp": "2024-11-10T20:33:38.818387", "username": "karoliukass"}
    ]

    chatters_amount = 300
    new_chatters_amount = 100
    message_amount = 3000
    unique_emote_amount = 100
    emote_amount = 3000
    
    person_who_mentioned_streamer_the_most_times = "Friebay"
    person_who_typed_the_most_emotes = "Tester"
    
    # Pass data to template
    return render_template('index.html', emotes=emotes, emotes_default=emotes_default,
                           top_chatters=top_chatters, top_emotes=top_emotes, subscirber_amount=subscirber_amount,
                           chatters_amount=chatters_amount, new_chatters_amount=new_chatters_amount,
                           message_amount=message_amount, unique_emote_amount=unique_emote_amount, emote_amount=emote_amount, 
                           person_who_mentioned_streamer_the_most_times=person_who_mentioned_streamer_the_most_times, person_who_typed_the_most_emotes=person_who_typed_the_most_emotes)

if __name__ == '__main__':
    app.run(debug=True)
