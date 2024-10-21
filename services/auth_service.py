from models.user_model import find_user, create_user
import bcrypt
import streamlit as st
import pymongo
import bcrypt
import re
from dotenv import load_dotenv
import os

# def login(email, password):
#     user = find_user(email)
#     if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
#         return True, "Login successful"
#     return False, "Invalid credentials"

# def register(email, password):
#     if find_user(email):
#         return False, "Email already exists"
#     create_user(email, password)
#     return True, "Registration successful"

# Load environment variables from .env file
load_dotenv()
# # MongoDB connection using URI directly
MONGODB_URI = "mongodb+srv://priy0023:priya@cluster0.16umr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGODB_DB = "priy0023"

# MongoDB connection setup using environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB")

# MongoDB connection setup with error handling
    try:
    client = pymongo.MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    collection = db["users"]
    st.write("Database connection successful!")
    except Exception as e:
    st.error(f"Error connecting to database: {e}")

    # Function to validate email
    def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

    # Function to validate password
    def is_valid_password(password):
    if len(password) < 12 or len(password) > 18:
    return False
    if not re.search("[a-zA-Z]", password) or not re.search("[0-9]", password):
    return False
    return True

    # Function to log in a user
    def login_user(email, password):
    user = collection.find_one({"email": email})
    if not user:
    return False, "User not found!"
    if bcrypt.checkpw(password.encode('utf-8'), user['password']):
    return True, "Login successful!"
    return False, "Invalid password!"

    # Function to register a user
    def register_user(email, password):
    if collection.find_one({"email": email}):
    return False, "User already exists!"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    collection.insert_one({"email": email, "password": hashed_password})
    return True, "User registered successfully!"
    # Initialize 'page' state if it's not already set
    if 'page' not in st.session_state:
    st.session_state.page = 'landing' # Default to landing page
