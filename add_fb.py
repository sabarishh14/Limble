import firebase_admin
from firebase_admin import credentials, db

if not firebase_admin._apps:
        cred = credentials.Certificate("credentials.json") 
        firebase_admin.initialize_app(cred, {"databaseURL": "https://limble-30e8a-default-rtdb.asia-southeast1.firebasedatabase.app/"})

def add_user(user_data,user_type):
    ref = db.reference('/')
    user_ref = ref.child(user_type) #or mentee
    user_ref.push().set(user_data)
    print(f"New {user_type} added successfully.")
