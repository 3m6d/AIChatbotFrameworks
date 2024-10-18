from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from nltk.corpus import stopwords
import nltk
import re

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Initialize stopwords for English
stop_words = set(stopwords.words('english'))
# Utility function to preprocess user input by removing stopwords and punctuation
def preprocess_input(text):
    # Remove punctuation and lowercase all words
    text = re.sub(r'[^\w\s]', '', text).lower()    
    # Tokenize and remove stop words
    tokens = [word for word in text.split() if word not in stop_words]
    
    # Join tokens back into a string
    return ' '.join(tokens)

def get_first_response(input_statement, response_list, storage=None):
    """
    Return the first response from the list of responses.
    """
    if response_list:
        return response_list[0]
    return None


# Create a chatbot instance with MongoDB adapter and multiple logic adapters
bot = ChatBot(
    "Fin",
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri='mongodb://localhost:27017/finbot',  # Ensure MongoDB is running
    logic_adapters=[
        "chatterbot.logic.BestMatch",  # Best match for FAQs
    ],
    read_only=False,  # Prevent writing to the database during conversations
)

# Training data
list_to_train = [
    "How to open a demat account?",
    "To open a demat account, you need to provide your citizenship number and PAN number.",
    "What is stock market?",
    "Stock market refers to the activities of buying and selling shares of a company.",
    "What is Nepal's capital market?",
    "Nepal's capital market consists of a primary market for new securities and a secondary market for trading existing securities, primarily facilitated through the Nepal Stock Exchange (NEPSE).",
    "What is the name of the Nepal Stock Exchange?",
    "The name of the Nepal Stock Exchange is NEPSE.",
    "What does NEPSE stand for?",
    "NEPSE stands for Nepal Stock Exchange.",
    "What is SEBON?",
    "SEBON refers to the Securities Board of Nepal, the regulatory body overseeing the securities market in Nepal.",
    "What is the role of SEBON in Nepal's capital market?",
    "SEBON regulates and supervises Nepal's securities market, ensuring investor protection and maintaining market integrity.",
    "What is an Initial Public Offering (IPO) in Nepal?",
    "An Initial Public Offering (IPO) in Nepal is the process through which a company offers its shares to the public for the first time.",
    "What is the Central Depository System (CDS) in Nepal?",
    "The Central Depository System (CDS) in Nepal is an electronic system that maintains and facilitates the ownership and transfer of securities in dematerialized form.",
    "What are the major financial institutions in Nepal?",
    "The major financial institutions in Nepal include commercial banks, development banks, finance companies, and microfinance institutions.",
    "What is the Nepal Rastra Bank?",
    "The Nepal Rastra Bank is the central bank of Nepal, responsible for monetary policy, regulation of financial institutions, and maintaining financial stability.",
    "What is the role of commercial banks in Nepal's financial system?",
    "Commercial banks in Nepal provide financial services such as deposits, loans, and other banking operations, playing a vital role in the country's economic growth.",
    "What is a Demat account?",
    "A Demat account is an account that allows investors to hold and trade securities in electronic form rather than in physical certificates.",
    "What is SourceCode Nepal?",
    "SourceCode Nepal is a financial technology company established with the aim of simplifying technology for capital markets. We are primarily focused on developing innovative technology products for stock brokers, merchant bankers, and stock investors.",
    "What is Smart Wealth?",
    "Smart Wealth Pro (SWP) is the stock market analysis software with multiple portfolio management services for Nepalese Stock Market investors, traders, and all stock market enthusiasts."
]

# Train the chatbot
list_trainer = ListTrainer(bot)
list_trainer.train(list_to_train)

# Chatbot loop
while True:
    try:
        # Get user input and preprocess it
        query = input("User: ").strip()

        if not query:
            print("Chatbot: Please ask a question!")
            continue
        
        # Preprocess user input to improve matching accuracy
        processed_query = preprocess_input(query)
        
        # Get response from the chatbot
        response = bot.get_response(processed_query)
        
        # Print chatbot response
        print("Chatbot: " + str(response))
        
        # Handle exit condition
        if query.lower() in ['quit', 'exit']:
            print("Chatbot: Goodbye!")
            break
        
    except (KeyboardInterrupt, EOFError, SystemExit):
        print("Chatbot: Goodbye!")
        break