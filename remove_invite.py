import firebase_admin
from firebase_admin import credentials, db

def remove_mentee_invite(mentor_email, mentee_email):
    if not firebase_admin._apps:
        cred = credentials.Certificate("credentials.json") 
        firebase_admin.initialize_app(cred, {"databaseURL": "https://limble-30e8a-default-rtdb.asia-southeast1.firebasedatabase.app/"})
    ref = db.reference('/')
    user_ref = ref.child("mentor")
    details = user_ref.get()
    invites_list = None  # Initialize invites_list as None
    flag = False
    for i in details:
        if details[i]["email"] == mentor_email and "invites" in details[i]:
            flag = True
            invites_list = details[i]["invites"]
            # Remove mentee's email from invites_list
            updated_invites_list = [invite for invite in invites_list if invite.get("email") != mentee_email]
            # Update invites_list in the database
            if updated_invites_list:
                # If updated invites list is not empty, update the invites key with the list
                user_ref.child(i).child("invites").set(updated_invites_list)
            else:
                # If updated invites list is empty, remove the invites key from the dictionary
                user_ref.child(i).child("invites").delete()
            break
    if flag:
        return updated_invites_list
    else:
        return []
