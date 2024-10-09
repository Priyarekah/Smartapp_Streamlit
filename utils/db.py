import json
import pandas as pd
import streamlit as st
from pymongo import MongoClient
from bson import ObjectId
from decimal import Decimal
from uuid import UUID
import datetime
import matplotlib.figure
import dill
# MongoDB connection setup
@st.cache_resource()
def mongodb_chat_connection():
    """
    Establishes a connection to the MongoDB chat database.
    """
    client = MongoClient(st.secrets["MONGODB_CHAT"]) 
    db = client[st.secrets["MONGO_DB"]] 
    collection = db["conversations"]  
    return collection

# Get the collection for chat history
collection = mongodb_chat_connection() 

# Pseudo owner ID for testing
pseudo_owner_id = ObjectId("60b8d295f1e7f3a9c5a73e56")

def get_conversations():
    """
    Retrieve all conversations from the MongoDB collection.
    """
    conversations = collection.find()  
    return list(conversations)  

def get_messages(conversation_id):
    """
    Retrieve messages for a given conversation ID.
    
    Parameters:
    conversation_id (str): The ID of the conversation.
    
    Returns:
    list: List of messages in the conversation.
    """
    conversation = collection.find_one({"_id": ObjectId(conversation_id)})  
    return conversation['messages']  

class JSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to handle types that the default encoder cannot.
    """
    def default(self, o):
        if isinstance(o, ObjectId): 
            return str(o)
        if isinstance(o, Decimal):  
            return float(o)
        if isinstance(o, UUID):  
            return str(o)
        return super().default(o)

def update_conversation(conversation_id, role, message_content, attachment_id=None):
    """
    Save messages to a given conversation in the MongoDB collection.
    
    Parameters:
    conversation_id (str): The ID of the conversation.
    role (str): The role of the message sender (e.g., 'user', 'assistant').
    message_content (str or pd.DataFrame): The content of the message.
    attachment_id (str, optional): The ID of the attachment.
    """
    format = "%Y-%m-%d %H:%M:%S"
    timeNow = datetime.datetime.strftime(datetime.datetime.now(),format)

    if isinstance(message_content, pd.DataFrame):  
        data = message_content.to_dict(orient='records')
        message_content = json.dumps(data, indent=4, cls=JSONEncoder)

    elif isinstance(message_content, matplotlib.figure.Figure):
        message_content = dill.dumps(message_content)

    new_message = {
        "role": role,  
        "owner_id": pseudo_owner_id,  
        "message_content": message_content,  
        "attachment_id": ObjectId(attachment_id) if attachment_id else None  
    }

    collection.update_one(
        {"_id": ObjectId(conversation_id)},
          {
            "$push": {"messages": new_message},
            "$set":{"timestamp": timeNow} 
        } 
    )

def delete_topic(topic):
    """
    Delete a document from the MongoDB collection by topic.
    
    Parameters:
    topic (str): The topic of the document to delete.
    
    Returns:
    str: Confirmation message of deletion or no document found.
    """
    result = collection.delete_one({"topic": topic}) 
    if result.deleted_count > 0:
        return f"Document with topic '{topic}' has been deleted."  
    else:
        return f"No document found with topic '{topic}'."
    

# Function to insert a new conversation
def insert_topic(role, topic, message):
    format = "%Y-%m-%d %H:%M:%S"
    new_conversation = {
        "topic": topic,
        "timestamp": datetime.datetime.strftime(datetime.datetime.now(datetime.timezone.utc),format),
        "messages": [
            {
                "role": role,
                "owner_id": pseudo_owner_id,
                "message_content": message,
                "attachment_id": None   
            }
        ]
    }
    collection.insert_one(new_conversation)


# Define a custom sorting function
def sort_by_date(item):
    # Convert the string to a datetime object using strptime
    date_obj = datetime.datetime.strptime(item["timestamp"], "%Y-%m-%d %H:%M:%S")
    return date_obj


