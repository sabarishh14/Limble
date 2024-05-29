import firebase_admin
from firebase_admin import credentials, db

def check_user(user_type,email,pwd):
    if not firebase_admin._apps:
        cred = credentials.Certificate("credentials.json") 
        firebase_admin.initialize_app(cred, {"databaseURL": "https://limble-30e8a-default-rtdb.asia-southeast1.firebasedatabase.app/",'storageBucket': 'limble-30e8a.appspot.com'})
    ref = db.reference('/')
    user_ref = ref.child(user_type) #or mentee
    details=user_ref.get()
    flag=0
    for i in details:
        if email==details[i]["email"] and pwd==details[i]["password"]:
            flag=1
            name=details[i]["name"]
            mentee_details=details[i]

    if flag==1:
        
        return [True,name,mentee_details]
    else:
        return [False]
