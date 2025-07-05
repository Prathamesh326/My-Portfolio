from flask import Flask, render_template, request, redirect, url_for
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')

@app.route("/contact", methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        sent = False
        error = None
        try:
            send_mail(name, email, subject, message)
            sent = True
        except Exception as e:
            error = str(e)
        return render_template("index.html", sent=sent, error=error, scroll_to_contact=True)
    return redirect(url_for('home'))

def send_mail(name, email, subject, message):
    email_message = f"Subject: {subject}\n\nName: {name}\nEmail: {email}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(EMAIL, EMAIL_PASSWORD)
        connection.sendmail(EMAIL, EMAIL, email_message)



