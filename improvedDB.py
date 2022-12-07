import openai
import os
import nltk 
import numpy as np 
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from pymongo import MongoClient

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = open_file('openaiapikey.txt')

# Create client
client = MongoClient('mongodb+srv://username:password!@myassistant.vadfb.mongodb.net/?retryWrites=true&w=majority')

# Connect to the database
db = client.myassistant.conversation

conversation = list()

# Insert document
db.conversations.insert_one({
    'logs': conversation
})

# Retrieve conversation logs
logs = db.conversations.find_one()['logs']

# NLP Feature Extraction
def featurize_sentence(sentence):
    words = nltk.word_tokenize(sentence)
    words = [word.lower() for word in words if word.isalpha()]
    return words

def create_feature_vectors(sentences):
    vectorizer = TfidfVectorizer(analyzer=featurize_sentence)
    feature_vectors = vectorizer.fit_transform(sentences)
    feature_vectors = feature_vectors.toarray()
    return feature_vectors

# Machine Learning Model
def create_model(feature_vectors, labels):
    x_train, x_test, y_train, y_test = train_test_split(feature_vectors, labels, test_size=0.2, random_state=42)
    log_reg = LogisticRegression(max_iter=1000)
    log_reg.fit(x_train, y_train)
    y_pred = log_reg.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    return log_reg, accuracy

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
    
# Saving Conversation Logs
def save_conversation_logs(conversation):
   # Create client
    client = MongoClient('mongodb+srv://norsninja:Panthera133!@myassistant.vadfb.mongodb.net/?retryWrites=true&w=majority')

# Connect to the database
    db = client.myassistant.conversation

def save_conversation_logs(conversation):
    # Insert document
    db.conversations.insert_one({
        'logs': conversation
    })

if __name__ == '__main__':
    # Retrieve conversation logs
    logs = db.conversations.find_one()['logs']

    conversation = list()
    while True:
        user_input = input('USER: ')
        conversation.append('USER: %s' % user_input)
        text_block = '\n'.join(conversation)
        prompt = open_file('prompt_chat.txt').replace('<<BLOCK>>', text_block)
        prompt = prompt + '\nJAX:'
        response = gpt3_completion(prompt)
        print('JAX:', response)
        conversation.append('JAX: %s' % response)
        save_conversation_logs(conversation)
