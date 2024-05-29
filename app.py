from flask import Flask, render_template, request, flash, redirect, url_for,jsonify
from skills_nlp import skills
from fb import add_user, check_user, link
from remove_invite import remove_mentee_invite
import invitesend
import webbrowser
import matching1
import getinvites
import inviteaccept
import getmatches
import ratementor

app = Flask(__name__)

user_type = None
registration_details = {}

global next_count
next_count=0

@app.route('/')
def index():
    return render_template('1splash.html')

@app.route('/splash', methods=['GET', 'POST'])
def splash():
    global user_type
    global registration_details
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        return render_template('2check.html')
    if request.method=="GET":
        return render_template('2check.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_type
    global registration_details
    global mentor_details
    global mentee_name
    global mentor_name
    global mentor_email
    global mentee_details_dict
    global mentor_details_dict
    global invite
    global mentee_email_1
    if request.method == 'POST':
        email = request.form.get('email')
        password=request.form.get('password')
        present=check_user(user_type,email,password)
        if present[0]:
            if user_type=="mentee":
                mentor_details=matching1.top_mentors_for_mentee(email)
                mentee_name=present[1]
                mentee_details_dict=present[2]
                mentee_email_1=email
                return render_template('message.html', message1="Successfully Logged In!", message2="Enjoy your session", page="dashboard") 
            elif user_type=="mentor":
                mentor_name=present[1]
                mentor_email=email
                invite=getinvites.get_invite(email)
                mentor_details_dict=present[2]
                return render_template('message.html', message1="Successfully Logged In!", message2="Enjoy your session", page="dashboard")   
        else:
            message1 = 'Invalid credentials. Please try again.'
            message2 = "Redirecting back to login page."
            return render_template('message.html', message1=message1, message2=message2, page="splash")  
    if request.method == 'GET':
        return render_template('3register.html')

@app.route('/register', methods=['POST'])
def register():
    global user_type
    global registration_details
    if request.method == 'POST':
        registration_details['email'] = request.form.get('email')
        registration_details['password'] = request.form.get('password')
        registration_details['name'] = request.form.get('name').title()
        registration_details['age'] = request.form.get('age')
        registration_details['languages'] = request.form.get('languages')
        registration_details['location'] = request.form.get('location').title()
        registration_details['gender'] = request.form.get('gender').title()
        image_file = request.files['image']
        registration_details['pic'] = link(image_file)
        return render_template(f'3msg_yourself_{user_type}.html')

@app.route('/msgy', methods=['GET', 'POST'])
def msgy():
    global user_type
    global registration_details
    if request.method == 'POST':
        registration_details['about_yourself'] = request.form.get('msg')
        if user_type=="mentor":
            registration_details["skills_expertise"]=skills(registration_details['about_yourself'])
            print(registration_details['skills_expertise'])
        elif user_type=="mentee":
            registration_details["skills_needed"]=skills(registration_details['about_yourself'])
            print(registration_details['skills_needed'])
        return render_template(f'4professional_details_{user_type}.html')

@app.route('/prof', methods=['GET', 'POST'])
def prof():
    global user_type
    global registration_details
    if request.method == 'POST':
        if user_type=="mentor":
            registration_details['field_of_work'] = request.form.get('field_of_work').title()
            registration_details['designation'] = request.form.get('designation').title() 
            registration_details['experience_level'] = request.form.get('experience_level').title()
            registration_details['linkedin'] = request.form.get('linkedin')
            registration_details['places_of_study'] = request.form.get('places_of_study')
            registration_details['places_of_work'] = request.form.get('places_of_work')
            add_user(registration_details,user_type)
            return render_template('message.html', message1=f"Welcome {registration_details['name']}.", message2="Successfully Created an account", page="prof")  
        elif user_type=="mentee":
            registration_details['current_skill_level'] = request.form.get('current_skill_level').title()
            registration_details['learning_style'] = request.form.get('learning_style').title()
            registration_details['expectations'] = request.form.get('expectations').title()
            registration_details['linkedin'] = request.form.get('linkedin')
            registration_details['places_of_study'] = request.form.get('places_of_study')
            add_user(registration_details,user_type)
            return render_template('message.html', message1=f"Welcome {registration_details['name']}.", message2="Successfully Created an account", page="prof")  
    if request.method=="GET":
        return render_template("2check.html")

@app.route('/dashboard')
def dashboard():
    global registration_details
    global mentor_details
    global mentee_dict
    if request.method=='GET':
        if user_type=="mentee":
            try:
                mentor_details=matching1.top_mentors_for_mentee(mentee_email_1)
                mentor_dict=mentor_details[next_count]
                mentor_skill_list=mentor_dict['skills_expertise'].split(', ')
            except:
                mentor_dict={}
                mentor_skill_list=[]
            return render_template('6dashboard.html',mentor_dict=mentor_dict,mentee_name=mentee_name,mentor_skill_list=mentor_skill_list)
        elif user_type=="mentor":
            invite=getinvites.get_invite(mentor_email)
            try:
                mentee_dict=invite[next_count]
                mentee_skill_list=mentee_dict['skills_needed'].split(', ')
            except:
                mentee_dict={}
                mentee_skill_list=[]
            return render_template('7dashboard.html',mentee_dict=mentee_dict,mentor_name=mentor_name,mentee_skill_list=mentee_skill_list)

@app.route('/rate_mentor', methods=['POST'])
def rate_mentor():
    mentor_name_2 = request.form.get('mentor_name')
    mentor_email_2=request.form.get('mentor_email')
    rating = request.form.get('rating')
    # Here you can add the logic to save the rating to a database or perform any other action
    ratementor.rate_mentor(mentor_email_2,rating)
    return render_template('message.html', message1=f"Mentor {mentor_name_2} rated successfully.", message2="Enjoy your session.", page="matches")   

@app.route('/dummydash',methods=['POST'])
def dummydash():
    global registration_details
    global mentor_details
    if request.method=='POST':
        name=request.form.get("mentee_name")
        for i in invite:
            if i['name']==name:
                mentee_dict=i
        mentee_skill_list=mentee_dict['skills_needed'].split(', ')
        return render_template('7dashboard.html',mentee_dict=mentee_dict,mentor_name=mentor_name,mentee_skill_list=mentee_skill_list)

@app.route('/dummydash2',methods=['POST'])
def dummydash2():
    global registration_details
    global mentor_details
    if request.method=='POST':
        name=request.form.get("mentor_name")
        for i in match:
            if i['name']==name:
                mentor_dict=i
        mentor_skill_list=mentor_dict['skills_expertise'].split(', ')
        return render_template('6dashboard.html',mentor_dict=mentor_dict,mentee_name=mentee_name,mentor_skill_list=mentor_skill_list)
    
@app.route('/send-invite', methods=['POST'])
def send_invite():
    global next_count
    if request.method == 'POST': 
            mentor_email=mentor_details[next_count]['email']
            invitesend.add_invite(mentor_email,mentee_details_dict)
            return render_template('message.html', message1="Invite Sent Successfully.", message2="Enjoy your session.", page="dashboard")   

@app.route('/reject-invite', methods=['POST'])
def reject_invite():
    global next_count
    if request.method == 'POST': 
            mentee_email=invite[next_count]['email']
            remove_mentee_invite(mentor_email,mentee_email)
            return render_template('message.html', message1="Invite Rejected!", message2="Check for other mentees", page="dashboard")   
    
@app.route('/accept-invite', methods=['POST'])
def accept_invite():
    global next_count
    if request.method == 'POST': 
            mentee_email=invite[next_count]['email']
            inviteaccept.accept_invite(mentee_email,mentor_details_dict)
            return render_template('message.html', message1="Invite accepted Successfully.", message2="Enjoy your session.", page="dashboard")   

    
@app.route('/next', methods=['POST'])     
def next():
    global next_count
    if request.method=='POST':
        if user_type=="mentee":
            next_count=(next_count + 1)%5
            return render_template('reload.html',page="dashboard")   
        elif user_type=="mentor":
            next_count=(next_count + 1)%len(invite)
            return render_template('reload.html',page="dashboard")  

@app.route('/logout', methods=['POST'])     
def logout():
    if request.method=='POST':
        return render_template('reload.html',page="")   

@app.route('/matches', methods=['POST',"GET"])     
def matches():
    global match
    match=getmatches.get_matches(mentee_email_1)
    if request.method=='POST':
        return render_template('matches.html',mentee_name=mentee_name,match=match) 
    elif request.method=='GET':
        print("hello")
        return render_template('matches.html',mentee_name=mentee_name,match=match) 

@app.route('/othermentee', methods=['POST'])     
def othermentee():
    invite=getinvites.get_invite(mentor_email)
    if request.method=='POST':
        return render_template('othermentees.html',mentor_name=mentor_name,invite=invite) 
      
@app.errorhandler(Exception)
def handle_error(error):
    return render_template("error.html", page="", error=str(type(error).__name__) + " – " + str(error))

if __name__ == '__main__':
    app.run()
