#   https://realpython.com/python-send-email/

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

# random_auth_code = random.randint(1000, 9999)

# def send_email(code):
#       print(code)


def send_email(code):
  sender_email = "keafakekea@gmail.com"
  receiver_email = "cristian.guba@gmail.com"
  password = "dtdathvnrstcpvqs"

  message = MIMEMultipart("alternative")
  message["Subject"] = "multipart test"
  message["From"] = sender_email
  message["To"] = receiver_email

# Create the plain-text and HTML version of your message
  text = """\
  Hi,
  Thank you.
  """

  html = f"""\
  <html>
    <body>
      <p>
        Hi,<br>
        <b>How are you?</b><br>
        Hi, your verification code is: {code}
      </p>
    </body>
  </html>
  """

# Turn these into plain/html MIMEText objects
  part1 = MIMEText(text, "plain")
  part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
  message.attach(part1)
  message.attach(part2)

  # Create secure connection with server and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      try:
          server.login(sender_email, password)
          server.sendmail(sender_email, receiver_email, message.as_string())
      except Exception as ex:
          print("ex")


# sender_email = "keafakekea@gmail.com"
# receiver_email = "cristian.guba@gmail.com"
# # password = "Bla!23cul"
# password = "dtdathvnrstcpvqs"
# message = MIMEMultipart("alternative")
# message["Subject"] = "multipart test"
# message["From"] = sender_email
# message["To"] = receiver_email
# #Create the plain-text and HTML version of your message
# text = """\
# Hi,
# Thank you.
# """
# html = f"""\
# <html>
#   <body>
#     <p>
#       Hi,<br>
#       <b>How are you?</b><br>
#       Hi, your verification code is: {random_auth_code}
#     </p>
#   </body>
# </html>
# """
# #Turn these into plain/html MIMEText objects
# part1 = MIMEText(text, "plain")
# part2 = MIMEText(html, "html")
# #Add HTML/plain-text parts to MIMEMultipart message
# #The email client will try to render the last part first
# message.attach(part1)
# message.attach(part2)
# # Create secure connection with server and send email
# context = ssl.create_default_context()
# with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#       server.login(sender_email, password)
#       server.sendmail(sender_email, receiver_email, message.as_string())
