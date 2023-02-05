# Imports
import openai
import os
import numpy as np 
# import pandas as pd
from pymongo import MongoClient
import random
import string
# import bs4

# File Functions
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# OpenAI Model
def gpt3_completion(prompt, engine='text-davinci-003', temp=0.7, top_p=1.0, tokens=1000, freq_pen=0.0, pres_pen=0.0, stop=['JAX:', 'USER:']):
    prompt = prompt.encode(encoding='utf- 8',errors='ignore').decode()
    # Check if prompt is too long
    if len(prompt) + tokens > 4097:
        # If too long, break up prompt into smaller chunks
        split_prompts = break_completion(prompt, max_tokens=4097-tokens)
        # Iterate through split prompts and get responses
        responses = []
        for split_prompt in split_prompts:
            try:
                response = openai.Completion.create(
                    engine=engine,
                    prompt=split_prompt,
                    temperature=temp,
                    max_tokens=tokens,
                    top_p=top_p,
                    frequency_penalty=freq_pen,
                    presence_penalty=pres_pen,
                    stop=stop)
            except openai.error.InvalidRequestError as e:
                print(e)
            except openai.error.TokenLimitError as e:
                print(e)
            except openai.error.InterruptedError as e:
                print(e)
            else:
                responses.append(response)
        # Join responses together
        text = ' '.join([resp['choices'][0]['text'].strip() for resp in responses])
    else:
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
        except openai.error.InvalidRequestError as e:
            print(e)
        except openai.error.TokenLimitError as e:
            print(e)
        except openai.error.InterruptedError as e:
            print(e)
        else:
            text = response['choices'][0]['text'].strip()
    return text

def break_completion(prompt, max_tokens, engine='text-davinci-003', temp=0.7, top_p=1.0, tokens=1000, freq_pen=0.0, pres_pen=0.0, stop=['JAX:', 'USER:']):
    split_prompts = list()
    token_count = 0
    # Check if length of prompt exceeds max token limit
    if len(prompt) > max_tokens:
        # If too long, break up prompt into smaller chunks
        split_prompts = prompt.split(' ')
    else:
        while token_count < max_tokens:
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
            except openai.error.InvalidRequestError as e:
                print(e)
            except Exception as e:
                print(e)
                break
            else:
                split_prompts.append(response)
                token_count += tokens
    return split_prompts

# Database Functions
# Create client
client = MongoClient('mongodb+srv://norsninja:ZS2S5Ydte8rnIZQf@myassistant.vadfb.mongodb.net/?retryWrites=true&w=majority')

# Connect to the database
db = client.myassistant.conversation

# Saving Conversation Logs
conversation = []
def save_conversation_logs(conversation):
    # Insert document
    
    db.conversations.insert_one({
        'logs': conversation
    })

class Assistant:
    def __init__(self):
        # Initialize OpenAI API Key
        openai.api_key = open_file('openaiapikey.txt')

    # Process user input and generate chatbot response
    def process_input(self, user_input):
        # Retrieve conversation logs
        logs = db.conversations.find_one()['logs']
        conversation = list()
        conversation.append('USER: %s' % user_input)
        text_block = '\n'.join(conversation)
        prompt = open_file('prompt_chat.txt').replace('<<BLOCK>>', text_block)
        prompt = prompt + '\nAssistant:'
        response = gpt3_completion(prompt)
        print('Assistant:', response)
         # Append the conversation logs with the new conversation
        logs.append(conversation) 
        #Insert the updated conversation logs
        db.conversations.insert_one({
            'logs': logs
        })
        return response



if __name__ == '__main__':
    openai.api_key = open_file('openaiapikey.txt')
    assistant1 = Assistant()


   
  # Retrieve conversation logs
    logs = db.conversations.find_one()['logs']
    
    while True:
        user_input = input('USER: ')
        response = assistant1.process_input(user_input)
