import firebase_admin
from firebase_admin import credentials, db

def accept_invite(mentee_email, mentor):
    if not firebase_admin._apps:
        cred = credentials.Certificate("credentials.json") 
        firebase_admin.initialize_app(cred, {"databaseURL": "https://limble-30e8a-default-rtdb.asia-southeast1.firebasedatabase.app/"})
    ref = db.reference('/')
    user_ref = ref.child("mentee")
    details = user_ref.get()
    flag = 0
    for i in details:
        if mentee_email == details[i]["email"]:
            if "matches" not in details[i]:
                details[i]["matches"] = []
            # Check if mentor already exists in the matches list
            if mentor not in details[i]["matches"]:
                details[i]["matches"].append(mentor)
                user_ref.update(details)
                flag = 1
                break
    if flag == 1:
        return True
    else:
        return False