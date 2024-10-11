import streamlit as st
import pymongo 
import bcrypt
# # MongoDB connection using URI directly
MONGODB_URI = "mongodb+srv://priy0023:priya@cluster0.16umr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGODB_DB = "priy0023"

# Initialize MongoDB client and access the database
client = pymongo.MongoClient(MONGODB_URI)  # Corrected to use parentheses
db = client[MONGODB_DB]
collection = db["users"]

# Function to register a user
def register_user(email, password):
    # Check if user already exists
    if collection.find_one({"email": email}):
        return False, "User already exists!"
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert user into the database
    user_data = {
        "email": email,
        "password": hashed_password
    }
    collection.insert_one(user_data)
    
    return True, "User registered successfully!"

# Function to log in a user
def login_user(email, password):
    # Find user by email
    user = collection.find_one({"email": email})
    
    if not user:
        return False, "User not found!"
    
    # Check if the provided password matches the stored hashed password
    if bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return True, "Login successful!"
    else:
        return False, "Invalid password!"

# Streamlit app layout
st.title("User Authentication App")

# Sidebar navigation
menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

# Register Page
if menu == "Register":
    st.subheader("Register")

    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    
    if st.button("Register"):
        if email and password:
            success, message = register_user(email, password)
            if success:
                st.success(message)
            else:
                st.error(message)
        else:
            st.error("Please provide both email and password!")

# Login Page
elif menu == "Login":
    st.subheader("Login")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login"):
        if email and password:
            success, message = login_user(email, password)
            if success:
                st.success(message)
            else:
                st.error(message)
        else:
            st.error("Please provide both email and password!")
