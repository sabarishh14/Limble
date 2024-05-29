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

'''print(add_invite("sarah@example.com", {
      "about_yourself": "I am abc, I am a software engineer and i know python and web development, i know to speak english and french",
      "age": "124",
      "current_skill_level": "Intermediate",
      "designation": "Des",
      "email": "abc@gmail.com",
      "expectations": "Ex",
      "experience_level": "Senior",
      "field_of_work": "Fow",
      "gender": "Male",
      "languages": "tamil",
      "learning_style": "Ls",
      "linkedin": "lin",
      "location": "Chennai",
      "name": "A",
      "password": "abc",
      "places_of_study": "sdf",
      "places_of_work": "pow",
      "skills_needed": "Web Development, Software Engineering, Python (Programming Language), English Language, French Language"
    }))'''