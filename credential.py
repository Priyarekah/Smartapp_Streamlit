import streamlit as st
import pymongo
import bcrypt
import re
from PIL import Image
from pages import registerlogin
from pages.register import registration_page
from pages.search import search_page
from pages.login import login_page
from pages.registerlogin import registerlogin_page

# MongoDB connection setup
MONGODB_URI = "mongodb+srv://priy0023:priya@cluster0.16umr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGODB_DB = "priy0023"

client = pymongo.MongoClient(MONGODB_URI)
db = client[MONGODB_DB]
collection = db["users"]

# Set up Streamlit page configuration
st.set_page_config(page_title="Smart Commute", layout="centered")

# Initialize the 'page' state if it's not already set
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# Landing Page
def landing_page():
    # Display images (ensure correct path handling depending on where images are stored)
    st.image("assets/images/top.png", use_column_width=True)
    st.image("assets/images/center.png", use_column_width=True)
    st.image("assets/images/bottom.png", use_column_width=True)

    # Button to start the app
    if st.button("Get Started"):
        # Set the session state to trigger page change
        st.session_state.page = 'registerlogin'
    
    # Immediately check if the state has changed and navigate
    if st.session_state.page == 'registerlogin':
        registerlogin_page()  # Trigger the register/login page

# Page Navigation Logic
def navigate():
    if st.session_state.page == 'landing':
        landing_page()
    elif st.session_state.page == 'registerlogin':
        registerlogin_page()  # Call the registerlogin page function
    elif st.session_state.page == 'register':
        registration_page()
    elif st.session_state.page == 'login':
        login_page()
    elif st.session_state.page == 'search':
        search_page()

# Call the navigation function to handle page switching
navigate()
