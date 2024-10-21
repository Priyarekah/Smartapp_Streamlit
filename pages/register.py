# Registration Page
import streamlit as st
import pymongo 
import re

MONGODB_URI = "mongodb+srv://priy0023:priya@cluster0.16umr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGODB_DB = "priy0023"


client = pymongo.MongoClient(MONGODB_URI)
db = client[MONGODB_DB]
collection = db["users"]


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