import os
import smtplib
from dotenv import load_env
from email.message import EmailMessage
from email.mime.text import MIMEText
from flask import Flask, render_template, request, url_for, redirect


load_env()

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/sendemail/", methods=['POST'])
def sendemail():
  if request.method ==  'POST':
    name = request.form['name']
    subject = request.form['subject']
    toEmail = request.form['_replyto']
    message = request.form['message']
    fromEmail = os.environ.get('PORTFOLIO_EMAIL_ADDR')
    pswd = os.environ.get('PORTFOLIO_EMAIL_PSWD')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(fromEmail, pswd)

    # Sender's and Receiver's email address
    msg = EmailMessage()
    msg.set_content(f"First Name : {name}\nEmail : {toEmail}\n\
                    Subject: {subject}\nMessage: {message}")

    msg['To'] = toEmail
    msg['From'] = fromEmail
    msg['Subject'] = subject

    try:
      server.send_message(msg)
      print("sent")
    except:
      print("failed to send")
      pass

  return redirect('/')

if __name__ == "__main__":
  app.run(debug=True)
