from flask import Flask, request, render_template, flash, url_for, redirect, session
from dbconnect import connection

from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc

app = Flask(__name__)

@app.route('/')
@app.route('/<user>')
def index(user=None):
    return render_template('user.html', user=user)

@app.route('/awesome/<int:ok>')
def awesome(ok):
    if ok<3:
        return "this is amazing"
    else:
        return "this is awesome"

@app.route('/method', methods=['POST','GET'])
def method():
    if request.method=='POST':
        return "you are posting!"
    else:
        return "you are getting!"

@app.route('/profile/<name>')
def profile(name):
    return render_template("profile.html", name=name)

@app.route('/shopping')
def shopping():
    food = ["chesscake", "beef", "indian buffet", "Chinese!"]
    return render_template('shopping.html', food= food)


@app.route('/register', methods=["GET","POST"])
def register_page():
    try:
        c, conn = connection()
        return("okay")
    except Exception as e:
        return(str(e))


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])


@app.route('/register1', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))

                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))


def after_this_request(f):
    if not hasattr(g, 'after_request_callbacks'):
        g.after_request_callbacks = []
    g.after_request_callbacks.append(f)
    return f

@app.before_request
def detect_user_language():
    language = request.cookies.get('user_lang')
    if language is None:
        language = guess_language_from_request()
        @after_this_request
        def remember_language(response):
            response.set_cookie('user_lang', language)
    g.language = language

if __name__ == '__main__':
    app.run(debug=True)



# below are hashing exmaples for future reference
# import hashlib
# password = 'pa$$w0rd'
# h = hashlib.md5(password.encode())
# print(h.hexdigest())
#
#
# user_entered_password = 'pa$$w0rd'
# salt = "5gz"
# db_password = user_entered_password+salt
# h = hashlib.md5(db_password.encode())
# print(h.hexdigest())
# ---------------------------
#
# from passlib.hash import sha256_crypt
#
# password = sha256_crypt.encrypt("password")
# password2 = sha256_crypt.encrypt("password")
#
# print(password)
# print(password2)
#
# print(sha256_crypt.verify("password", password))
#
