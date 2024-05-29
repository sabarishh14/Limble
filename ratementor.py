import firebase_admin
from firebase_admin import credentials, db

def rate_mentor(mentor_email, rating):
    if not firebase_admin._apps:
        cred = credentials.Certificate("credentials.json") 
        firebase_admin.initialize_app(cred, {"databaseURL": "https://limble-30e8a-default-rtdb.asia-southeast1.firebasedatabase.app/"})
    ref = db.reference('/')
    user_ref = ref.child("mentor")
    details = user_ref.get()
    flag = 0
    
    for i in details:
        if mentor_email == details[i]["email"]:
            if "rating" not in details[i]:
                details[i]["rating"] = str(rating)
            else:
                details[i]['rating']=(float(details[i]['rating'])+float(rating))/2
            # Check if mentee already exists in the invites list
            user_ref.update(details)

            flag = 1
            break
    if flag == 1:
        return True
    else:
        return False