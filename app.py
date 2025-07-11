from flask import Flask, render_template, request, redirect, url_for
import smtplib
import os
from dotenv import load_dotenv
import logging

load_dotenv()
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

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
    confirmation_subject = "Thank you for contacting Prathamesh Shinde"
    confirmation_message = f"Subject: {confirmation_subject}\n\nDear {name},\n\nThank you for reaching out! I have received your message and will get back to you soon.\n\nBest regards,\nPrathamesh Shinde"
    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(EMAIL, EMAIL_PASSWORD)
            # Send email to site owner
            connection.sendmail(EMAIL, EMAIL, email_message)
            logging.info(f"Contact email sent to site owner from {email} (name: {name}, subject: {subject})")
            # Send confirmation to user
            connection.sendmail(EMAIL, email, confirmation_message)
            logging.info(f"Confirmation email sent to user at {email} (name: {name})")
    except Exception as e:
        logging.error(f"Error sending email(s): {e}")
        raise



