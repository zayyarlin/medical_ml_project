# -*- coding: utf-8 -*-

from scripts import tabledef
from scripts import forms
from scripts import helpers
from flask import Flask, redirect, url_for, render_template, request, session, jsonify
import json
import sys
import os
import stripe
import pickle

app = Flask(__name__)
# model = pickle.load(open('model.pkl','rb'))
app.secret_key = os.urandom(12)  # Generic key for dev purposes only

stripe_keys = {
  'secret_key': os.environ['STRIPE_SECRET_KEY'],
  'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

# Heroku
#from flask_heroku import Heroku
#heroku = Heroku(app)

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def login():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = request.form['password']
            if form.validate():
                if helpers.credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    session['password'] = password
                    return json.dumps({'status': 'Login successful'})
                return json.dumps({'status': 'Invalid user/pass'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    user = helpers.get_user()
    return render_template('home.html', user=user)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = ""
    session['password'] = ""
    return redirect(url_for('login'))


# -------- Signup ---------------------------------------------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = helpers.hash_password(request.form['password'])
            email = request.form['email']
            if form.validate():
                if not helpers.username_taken(username):
                    helpers.add_user(username, password, email)
                    session['logged_in'] = True
                    session['username'] = username
                    session['password'] = password
                    return json.dumps({'status': 'Signup successful'})
                return json.dumps({'status': 'Username taken'})
            return json.dumps({'status': 'User/Pass required'})
        return render_template('login.html', form=form)
    return redirect(url_for('login'))


# -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
            session['password'] = password
            return json.dumps({'status': 'Saved'})
        user = helpers.get_user()
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))


# -------- Payment with stripe ---------------------------------------------- #
@app.route('/payment')
def payment():
    if session.get('logged_in'):
        user = helpers.get_user()
        return render_template('payment.html', key=stripe_keys['publishable_key'], user=user)
    else:
        return redirect(url_for('login'))


@app.route('/charge', methods=['POST'])
def charge():
    if session.get('logged_in'):
        user = helpers.get_user()
        try:
            amount = 2000   # amount in cents
            customer = stripe.Customer.create(
                email=user.email,
                source=request.form['stripeToken']
            )
            stripe.Charge.create(
                customer=customer.id,
                amount=amount,
                currency='usd',
                description='Better Doctor Charge'
            )
        except stripe.error.StripeError:
            return render_template('error.html')
        helpers.change_user(paid=True)

    # This is confusing at the moment because main page is routed by login
    return redirect(url_for('login'))

# -------- Chat Main Page ---------------------------------------------- #
# TODO

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)
    if helpers.credentials_valid_paid(data['username'], data['password']) or int(data['patient'])<2:
        print(data)
        # prediction = model.predict(data['message'])
        # output = prediction[0]
        # return jsonify(output)
        return jsonify({"message": f"You said {data['message']}"})
    else:
        return jsonify({"message": "You need to pay to use this"})

@app.route('/patient/<number>', methods=['GET'])
def patient(number):
    if session.get("logged_in"):
        return render_template('chat.html', id=number, username = session['username'], password = session['password']  )
    else:
        return redirect(url_for("login"))

# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=80, host='0.0.0.0')
