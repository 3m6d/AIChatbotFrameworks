import requests
import os
import logging
import wit

# Set up your Wit.ai access token
access_token = os.getenv('WIT_ACCESS_TOKEN', '4AAJZIDXAXDRR7M6DIY5F4WJKFS4XJUL')

wit_client = wit.Wit(access_token)

# Set headers
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

def get_wit_response(message_text):
    """
    Queries Wit.ai servers with the given message text and returns entity and intent.

    :param message_text: The text to query Wit.ai with.
    :return: The parsed JSON response from the Wit.ai server or None if there is an error.
    """
    # Format the Wit.ai API URL with the message text
    url = f'https://api.wit.ai/message?v=20240910&q={message_text}'
    
    try:
        # Make the GET request to Wit.ai
        response = wit_client.message(message_text)
        #response = requests.get(url, headers=headers)
        intent = response['intents'][0]['name'] if response['intents'] else None
        entities = response['entities']
        return intent, entities
    except Exception as e:
        print(f"Error communicating with Wit.ai: {e}")
        return None, None       
         #response.raise_for_status()  # Raise an exception for HTTP errors
        #data = response.json()

        # Log and return the successful response
        logging.info(f"Wit.ai response: {data}")
        return data
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
    return None

# Example usage (you can remove this or use it for testing):
if __name__ == "__main__":
    user_message = "How do I open a Demat account?"
    wit_response = get_wit_response(user_message)
    if wit_response:
        print(wit_response)
    else:
        print("Failed to get a response from Wit.ai")
