from flask import Flask, render_template, request, redirect, session, url_for
import re

app = Flask(__name__)
app.secret_key = 'supersecret'

# Dummy user database
users = {}

# Email regex for Gmail/Outlook
EMAIL_REGEX = re.compile(r'^.*@(gmail\.com|outlook\.com)$')

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    if not EMAIL_REGEX.match(email):
        return "Only Gmail or Outlook emails allowed."
    password = request.form['password']
    if users.get(email) == password:
        session['user'] = email
        return redirect(url_for('dashboard'))
    return "Invalid credentials."

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    if not EMAIL_REGEX.match(email):
        return "Only Gmail or Outlook emails allowed."
    password = request.form['password']
    users[email] = password
    session['user'] = email
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
