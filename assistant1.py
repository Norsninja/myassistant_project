# Imports
import openai
import os
import numpy as np 
from pymongo import MongoClient
from mongo_connection import db
import random
import string

# File Functions
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# OpenAI Model
def gpt3_completion(prompt, engine='text-davinci-003', temp=0.7, top_p=1.0, tokens=1000, freq_pen=0.0, pres_pen=0.0, stop=['JAX:', 'USER:']):
    max_retry = 1
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
        except openai.error.InvalidRequestError as e:
            print(e)
        except openai.error.TokenLimitError as e:
            print(e)
        except openai.error.InterruptedError as e:
            print(e)
        else:
            return text
        retry += 1
        if retry >= max_retry:
            return None


class Assistant:
    def __init__(self):
        # Initialize OpenAI API Key
        openai.api_key = open_file('openaiapikey.txt')
        self.conversation = list()

    # Process user input and generate chatbot response
    def process_input(self, user_input):
        # Append the user input to the conversation logs
        self.conversation.append('USER: %s' % user_input)
        text_block = '\n'.join(self.conversation)
        prompt = open_file('prompt_chat.txt').replace('<<BLOCK>>', text_block)
        prompt = prompt + '\nAssistant:'
        response = gpt3_completion(prompt)
        print('Assistant:', response)
        # Append the Assistant response to the conversation logs
        self.conversation.append('Assistant: %s' % response)
       
        return response
        



if __name__ == '__main__':
    openai.api_key = open_file('openaiapikey.txt')
    
    # Retrieve conversation logs
    logs = db.conversations.find_one()['logs']

   # conversation = list()
  