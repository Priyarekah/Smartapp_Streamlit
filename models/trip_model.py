def save_trip(email, trip_data):
    return db.users.update_one({"email": email}, {"$push": {"history": trip_data}})

def get_user_trips(email):
    user = db.users.find_one({"email": email})
    return user.get("history", [])
