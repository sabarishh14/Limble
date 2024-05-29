import firebase_admin
from firebase_admin import credentials, db

def add_invite(mentor_email, mentee):
    if not firebase_admin._apps:
        cred = credentials.Certificate("credentials.json") 
        firebase_admin.initialize_app(cred, {"databaseURL": "https://limble-30e8a-default-rtdb.asia-southeast1.firebasedatabase.app/"})
    ref = db.reference('/')
    user_ref = ref.child("mentor")
    details = user_ref.get()
    flag = 0
    for i in details:
        if mentor_email == details[i]["email"]:
            if "invites" not in details[i]:
                details[i]["invites"] = []
            # Check if mentee already exists in the invites list
            if mentee not in details[i]["invites"]:
                details[i]["invites"].append(mentee)
                user_ref.update(details)
                flag = 1
                break
    if flag == 1:
        return True
    else:
        return False