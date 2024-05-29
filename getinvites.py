import firebase_admin
from firebase_admin import credentials, db

def get_invite(mentor_email):
    if not firebase_admin._apps:
        cred = credentials.Certificate("credentials.json") 
        firebase_admin.initialize_app(cred, {"databaseURL": "https://limble-30e8a-default-rtdb.asia-southeast1.firebasedatabase.app/"})
    ref = db.reference('/')
    user_ref = ref.child("mentor")
    details = user_ref.get()
    invites_list = None  # Initialize invites_list as None
    flag=0
    for i in details:
        if mentor_email == details[i]["email"]:
            if "invites" in details[i]: 
                flag=1 # Check if "invites" key exists
                invites_list = details[i]["invites"]
            break
    if flag==1:
        return invites_list
    else:
        return []
