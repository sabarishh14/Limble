import firebase_admin
from firebase_admin import credentials, db

def get_matches(mentee_email):
    if not firebase_admin._apps:
        cred = credentials.Certificate("credentials.json") 
        firebase_admin.initialize_app(cred, {"databaseURL": "https://limble-30e8a-default-rtdb.asia-southeast1.firebasedatabase.app/"})
    ref = db.reference('/')
    user_ref = ref.child("mentee")
    details = user_ref.get()
    matches_list = None  # Initialize matches_list as None
    flag=0
    for i in details:
        if mentee_email == details[i]["email"]:
            if "matches" in details[i]: 
                flag=1 # Check if "invites" key exists
                matches_list = details[i]["matches"]
            break
    if flag==1:
        return matches_list
    else:
        return []
