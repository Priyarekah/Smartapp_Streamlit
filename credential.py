# import streamlit as st
# import pymongo 
# import bcrypt
# # # MongoDB connection using URI directly
MONGODB_URI = "mongodb+srv://priy0023:priya@cluster0.16umr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGODB_DB = "priy0023"

# # Initialize MongoDB client and access the database
# client = pymongo.MongoClient(MONGODB_URI)  # Corrected to use parentheses
# db = client[MONGODB_DB]
# collection = db["users"]

# # Function to register a user
# def register_user(email, password):
#     # Check if user already exists
#     if collection.find_one({"email": email}):
#         return False, "User already exists!"
    
#     # Hash the password
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#     # Insert user into the database
#     user_data = {
#         "email": email,
#         "password": hashed_password
#     }
#     collection.insert_one(user_data)
    
#     return True, "User registered successfully!"

# # Function to log in a user
# def login_user(email, password):
#     # Find user by email
#     user = collection.find_one({"email": email})
    
#     if not user:
#         return False, "User not found!"
    
#     # Check if the provided password matches the stored hashed password
#     if bcrypt.checkpw(password.encode('utf-8'), user['password']):
#         return True, "Login successful!"
#     else:
#         return False, "Invalid password!"

# # Streamlit app layout
# st.title("User Authentication App")

# # Sidebar navigation
# menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

# # Register Page
# if menu == "Register":
#     st.subheader("Register")

#     email = st.text_input("Email", key="register_email")
#     password = st.text_input("Password", type="password", key="register_password")
    
#     if st.button("Register"):
#         if email and password:
#             success, message = register_user(email, password)
#             if success:
#                 st.success(message)
#             else:
#                 st.error(message)
#         else:
#             st.error("Please provide both email and password!")

# # Login Page
# elif menu == "Login":
#     st.subheader("Login")

#     email = st.text_input("Email", key="login_email")
#     password = st.text_input("Password", type="password", key="login_password")
    
#     if st.button("Login"):
#         if email and password:
#             success, message = login_user(email, password)
#             if success:
#                 st.success(message)
#             else:
#                 st.error(message)
#         else:
#             st.error("Please provide both email and password!")


import streamlit as st
import pymongo
import bcrypt
import re
from PIL import Image

# MongoDB connection setup
# MONGODB_URI = "your_mongodb_uri"
# MONGODB_DB = "your_database_name"

client = pymongo.MongoClient(MONGODB_URI)
db = client[MONGODB_DB]
collection = db["users"]

# Set up Streamlit page configuration
st.set_page_config(page_title="Smart Commute", layout="centered")

# Initialize the 'page' state if it's not already set
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

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

# Landing Page
def landing_page():
    st.title("Welcome to Smart Commute")
    st.image("/home/priya/Android/Smartapp_Streamlit/assets/images/top.png", use_column_width=True)
    st.image("/home/priya/Android/Smartapp_Streamlit/assets/images/center.png", use_column_width=True)
    st.image("/home/priya/Android/Smartapp_Streamlit/assets/images/bottom.png", use_column_width=True)

    # GPS Permissions Check Placeholder
    if st.button("Grant GPS Permissions"):
        st.session_state.gps_permission = True  # This should handle actual GPS logic

    # Language Selection
    languages = ["English", "Malay", "Mandarin", "Tamil"]
    selected_language = st.selectbox("Select Language", languages)
    st.session_state.language = selected_language  # This should handle translation logic

    # Navigation to Login or Register
    menu = st.radio("Choose an option", ["Register", "Sign In"])
    if menu == "Register":
        st.session_state.page = "register"
    elif menu == "Sign In":
        st.session_state.page = "login"

# Registration Page
def registration_page():
    st.title("Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not is_valid_email(email):
            st.error("Invalid Email")
        elif not is_valid_password(password):
            st.error("Invalid Password")
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            collection.insert_one({"email": email, "password": hashed_password})
            st.success("Registration successful! Please check your email for verification.")
            st.session_state.page = 'landing'

    if st.button("Back to Landing"):
        st.session_state.page = 'landing'

# Login Page
def login_page():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = collection.find_one({"email": email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            st.success("Login successful!")
            st.session_state.page = 'search'  # Redirect to Search Page
        else:
            st.error("Invalid email or password.")

    if st.button("Forgot Password"):
        # Logic for sending password reset link
        st.success("Password reset link sent to your email!")

    if st.button("Back to Landing"):
        st.session_state.page = 'landing'

# Search Page
def search_page():
    st.title("Search Locations")
    start_location = st.text_input("Starting Location")
    destination_location = st.text_input("Destination Location")

    if st.button("Search"):
        if start_location and destination_location:
            # Logic for querying transportation options would go here
            st.success("Searching for options...")
            st.session_state.page = 'travel_comparison'  # Redirect to comparison page
        else:
            st.error("Please enter both locations.")

    if st.button("Back to Landing"):
        st.session_state.page = 'landing'

# Page Navigation Logic
if st.session_state.page == 'landing':
    landing_page()
elif st.session_state.page == 'register':
    registration_page()
elif st.session_state.page == 'login':
    login_page()
elif st.session_state.page == 'search':
    search_page()
# You can continue adding more pages for Travel Comparison, User Preferences, etc.
