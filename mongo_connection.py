from pymongo import MongoClient

# Create client
client = MongoClient('mongodb+srv://norsninja:ZS2S5Ydte8rnIZQf@myassistant.vadfb.mongodb.net/?retryWrites=true&w=majority')

# Connect to the database
db = client.myassistant.conversation
