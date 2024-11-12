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

    # Convert data to dictionaries for easy template rendering
    emotes = emotes.to_dict(orient='records')
    emotes_default = emotes_default.to_dict(orient='records')
    top_chatters = top_chatters.to_dict(orient='records')
    top_emotes = top_emotes.to_dict(orient='records')

    # Pass data to template
    return render_template('outro.html', emotes=emotes, emotes_default=emotes_default,
                           top_chatters=top_chatters, top_emotes=top_emotes)

if __name__ == '__main__':
    app.run(debug=True)
