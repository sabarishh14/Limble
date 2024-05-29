# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# def send_email(sender_email, sender_password, receiver_email, subject, message):
#     # Setup the MIME
#     message = MIMEMultipart()
#     message['From'] = sender_email
#     message['To'] = receiver_email
#     message['Subject'] = subject
    
#     # Add body to email
#     message.attach(MIMEText(message, 'plain'))
    
#     # Connect to the SMTP server
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.starttls()
    
#     # Login to the SMTP server
#     server.login(sender_email, sender_password)
    
#     # Send the email
#     text = message.as_string()
#     server.sendmail(sender_email, receiver_email, text)
    
#     # Close the SMTP server
#     server.quit()

# # Example usage
# sender_email = "limble.corp@gmail.com"
# sender_password = "limble123"
# receiver_email = "sbsabarish14@gmail.com"
# subject = "You got an invite!"
# message = "TWelcome to Limble"

# send_email(sender_email, sender_password, receiver_email, subject, message)

# import smtplib, ssl

# port = 465  # For SSL
# smtp_server = "smtp.gmail.com"
# sender_email = "limble.corp@gmail.com"  # Enter your address
# receiver_email = "sbsabarish14@gmail.com"  # Enter receiver address
# password = "limble123"
# message = """\
# You got an invite!

# TWelcome to Limble"""

# context = ssl.create_default_context()
# with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#     server.login(sender_email, password)
#     server.sendmail(sender_email, receiver_email, message)

# # smtplib module send mail

# import smtplib

# TO = "sbsabarish14@gmail.com"
# SUBJECT = 'TEST MAIL'
# TEXT = 'Here is a message from python.'

# # Gmail Sign In
# gmail_sender = "limble.corp@gmail.com" 
# gmail_passwd = "limble123"

# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.ehlo()
# server.starttls()
# server.login(gmail_sender, gmail_passwd)

# BODY = '\r\n'.join(['To: %s' % TO,
#                     'From: %s' % gmail_sender,
#                     'Subject: %s' % SUBJECT,
#                     '', TEXT])

# try:
#     server.sendmail(gmail_sender, [TO], BODY)
#     print ('email sent')
# except:
#     print ('error sending mail')


import smtplib
from email.mime.text import MIMEText

subject = "Email Subject"
body = "This is the body of the text message"
sender = "limble.corp@gmail.com"
recipients = ["sbsabarish14@gmail.com"]
password = "limble123"


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")


send_email(subject, body, sender, recipients, password)