from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import nltk
from pymongo import MongoClient


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Set up ChatterBot with local MongoDB as the storage adapter
chatbot = ChatBot(
    'FinBot',
    read_only=False,
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri='mongodb://localhost:27017/finbot',  # Adjust the URI to point to your local MongoDB
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'It seems I am still learning and cannot answer it right now.',
            'maximum_similarity_threshold': 0.9
        }
    ]
)

print("------------ FinBot ------------")

# MongoDB setup for accessing the financial FAQs collection
client = MongoClient('mongodb://localhost:27017/')
db = client['finbot']  # The database name
faq_collection = db['financial_faqs']  # The collection where the financial FAQs are stored
conversation_collection = db['conversations']

# Train the chatbot with ChatterBot's corpus data
corpus_trainer = ChatterBotCorpusTrainer(chatbot)
corpus_trainer.train("chatterbot.corpus.english")

# List of training data
list_to_train = [
    "What is Nepal's capital market?", 
    "Nepal's capital market consists of a primary market for new securities and a secondary market for trading existing securities, primarily facilitated through the Nepal Stock Exchange (NEPSE).",
    # Add more Q&A pairs as needed
]

# Train the chatbot with custom financial questions and answers
list_trainer = ListTrainer(chatbot)
list_trainer.train(list_to_train)

def get_faq_response_from_mongo(intent, entities):
    """
    Search the database (MongoDB) for a response matching the intent and entities.
    """
    # For example, use the intent and entities to search MongoDB
    faq = faq_collection.find_one({"intent": intent, "entities": entities})
    
    if faq:
        return faq['response']  # Return answer if found
    return None

def store_conversation(user_input, bot_response, intent=None, entities=None):
    """
    Store every conversation in MongoDB.
    """
    conversation = {
        "user_input": user_input,
        "bot_response": bot_response,
        "intent": intent,
        "entities": entities
    }
    conversation_collection.insert_one(conversation)

def get_chatbot_response(user_input):
    """
    Main function to handle response retrieval from MongoDB or ChatterBot fallback.
    """
    # Try to get a response from MongoDB's financial FAQs first (if intent and entities are known)
    faq_response = get_faq_response_from_mongo(None, None)

    # If an FAQ response is found in MongoDB, return it
    if faq_response:
        return faq_response

    # If no FAQ response found, use ChatterBot as a fallback
    chatterbot_response = str(chatbot.get_response(user_input))

    # Store the conversation in MongoDB for future training
    store_conversation(user_input, chatterbot_response)
    
    return chatterbot_response

# Example usage:
if __name__ == "__main__":
    while True:
        user_message = input("What can I help you with today? :")
        response = get_chatbot_response(user_message)
        print(f"Chatbot: {response}")
