#!/usr/bin/python3.6
from flask import Flask
import sys, os
from flask_mail import Mail
from admin.routes import admin
from student.routes import student
from main.routes import main

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nilekrator'
app.config['USERNAME'] = os.environ['USERNAME']
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')

mail = Mail(app)

app.register_blueprint(admin)
app.register_blueprint(student)
app.register_blueprint(main)

if __name__ == '__main__':
    info = sys.version_info

    if info.major < 3:
        print("Python version 3.x or higher is recommended\n")

    app.run(debug=True, port=80)
