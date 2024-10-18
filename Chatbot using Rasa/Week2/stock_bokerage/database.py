from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['finbot']
collection = db['financial_faqs']

def search_mongo(intent, entities):
    # Base query to search for the intent
    query = {"intent": intent}
    
    # Optionally, add entities to the query if available
    if entities:
        # Extract relevant entities from the wit.ai response
        entity_filter = {}
        for entity_name, entity_data in entities.items():
            entity_value = entity_data[0]['value']  # Get the first value for each entity
            entity_filter[entity_name.split(":")[0]] = entity_value  # Remove the role from the entity key
            
        query["entities"] = entity_filter

    # Search for a matching document in MongoDB
    response_doc = collection.find_one(query)
    
    # Return the response if found, otherwise a fallback message
    if response_doc:
        return response_doc.get('response', "Sorry, I don't have a response for that.")
    else:
        return "Sorry, I couldn't find any information related to your query."

# Example usage
intent = "Demat_account_query"
entities = {
    'account_type:account_type': [{'value': 'demat'}],
    'action:action': [{'value': 'open'}]
}

# Search for response in MongoDB
response = search_mongo(intent, entities)
print(response)
