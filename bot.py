# from flask import Flask, render_template, request, jsonify
# import random
# import json
# import os
# from fuzzywuzzy import fuzz

# app = Flask(__name__)

# # Load training data
# data_path = os.path.join(os.path.dirname(__file__), 'train_data.json')
# with open(data_path, 'r', encoding='utf-8') as f:
#     responses = json.load(f)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/get', methods=['POST'])
# def get_bot_response():
#     user_msg = request.json['msg'].lower().strip()
#     reply = "I'm not sure how to respond to that."

#     best_score = 0
#     best_key = None

#     for pattern in responses.keys():
#         score = fuzz.partial_ratio(pattern.lower(), user_msg)
#         if score > best_score:
#             best_score = score
#             best_key = pattern

#     if best_score >= 70:  # Match threshold
#         reply = random.choice(responses[best_key])

#     return jsonify({'reply': reply})

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import random
import json
import difflib

app = Flask(__name__)

# Load training data
with open('train_data.json', encoding='utf-8') as f:
    responses = json.load(f)

# Track user language preference (for simplicity, using global variable here)
user_language = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def get_bot_response():
    user_msg = request.json['msg'].strip().lower()

    session_id = request.remote_addr  # unique per user (simple method)

    # If user hasn't picked a language yet
    if session_id not in user_language:
        if 'english' in user_msg:
            user_language[session_id] = 'english'
            return jsonify({'reply': "Great! How can I help you?"})
        elif 'marathi' in user_msg or 'मराठी' in user_msg:
            user_language[session_id] = 'marathi'
            return jsonify({'reply': "छान! मला सांगा, मी कशी मदत करू शकतो?"})
        else:
            return jsonify({'reply': "Please choose a language: English or मराठी (Marathi)"})

    lang = user_language[session_id]
    reply = "I'm not sure how to respond to that." if lang == 'english' else "माफ करा, मला उत्तर देता आले नाही."

    # Find closest key match
    for pattern in responses:
        matches = difflib.get_close_matches(pattern, [user_msg], n=1, cutoff=0.6)
        if matches:
            reply = random.choice(responses[pattern])
            break

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
