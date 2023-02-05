# Imports
from flask import Flask, render_template, request, redirect, flash, jsonify
import openai
import assistant1
import logging
from assistant1 import gpt3_completion
from pymongo import MongoClient
from mongo_connection import db

# Instantiate an object of the assistant1 module
assistant1 = assistant1.Assistant()

# File Functions
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Flask app
app = Flask(__name__)
app.secret_key = '123456789'

# App routes
@app.route('/', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'GET':
        # Retrieve conversation logs
        logs = db.conversations.find_one()['logs']
        return render_template('index.html', conversation=logs, public=True)
    if request.method == 'POST':
        user_input = unquote(request.form['user_input'])
        print('User: ' + user_input)
        # Output user prompt in the browser window
        flash(user_input, category='user_input')

        # Process user input and generate chatbot response
        response = assistant1.process_input(user_input)
        flash(response, category='response')
 
        # Retrieve conversation logs
        logs = db.conversations.find_one()['logs']

        # Pass conversation logs to index.html:
        return render_template('index.html', conversation=logs, public=True, user_input=user_input, response=response)
        # return redirect(url_for('chatbot'))

@app.route('/update_conversation', methods=['POST'])
def update_conversation():
    logs = logging.getLogger(__name__)
    user_input = request.form['user_input']
    logs.info('User: ' + user_input)

    # Get chatbot response
    response = assistant1.process_input(user_input)

    # Update conversation logs in database
    db.conversations.update_one({}, {'$push': {'logs': {'user': user_input, 'Assistant': response}}})

    # Return response
    return response

# Run app
if __name__ == '__main__':
    app.run(debug=True)
