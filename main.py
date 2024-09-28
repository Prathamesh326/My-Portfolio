from flask import Flask, render_template, request
import smtplib

EMAIL = "pratzz326@gmail.com"
PASSWORD = "qbtzclchghuvkjpx"

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/education")
def education():
    return render_template("education.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/certifications")
def certifications():
    return render_template("certifications.html")


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        send_mail(name, email, subject, message)

        return render_template("contact.html", sent=True)
    return render_template("contact.html")


def send_mail(name, email, subject, message):
    email_message = f"Subject: {subject}\n\nName: {name}\nEmail: {email}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        connection.sendmail(EMAIL, PASSWORD, email_message)


if __name__ == '__main__':
    app.run(debug=True)
