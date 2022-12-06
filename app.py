from flask import Flask, request

app = Flask(__name__)

def get_chatbot_response(user_input):
    # Add code to send user_input to chatbot and store response
    response = 'Chatbot response'
    return response

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('userInput')
        response = get_chatbot_response(user_input)
        return response
    else:
        return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)
