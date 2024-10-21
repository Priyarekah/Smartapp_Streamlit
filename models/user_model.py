from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb://localhost:27017/")
db = client.smartcommute

def create_user(email, password):
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {
        "email": email,
        "password": hashed_pw,
        "preferences": {},
        "history": []
    }
    return db.users.insert_one(user)

def find_user(email):
    return db.users.find_one({"email": email})

def update_preferences(email, preferences):
    return db.users.update_one({"email": email}, {"$set": {"preferences": preferences}})
