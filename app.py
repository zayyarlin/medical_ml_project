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
import requests

app = Flask(__name__)
# model = pickle.load(open('model.pkl','rb'))
app.secret_key = os.urandom(12)  # Generic key for dev purposes only

stripe_keys = {
  'secret_key': os.environ['STRIPE_SECRET_KEY'],
  'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}

qa_svce_host = os.environ['QA_SVCE_HOST']
qa_svce_port = os.environ['QA_SVCE_PORT']

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
    return render_template('home.html', user=user, patients=helpers.get_patients())


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
                session['password'] = request.form['password']
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
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
            return render_template('error.html',user=user)
        helpers.change_user(paid=True)

    # This is confusing at the moment because main page is routed by login
    return redirect(url_for('login'))

# -------- Chat Main Page ---------------------------------------------- #

@app.route('/chat', methods=['POST'])
def chat():
    if session.get("logged_in"):
        user = helpers.get_user()
        content = request.json
        patient_id = content['patient_id']
        question  = content['message']
        patient = helpers.get_patient(int(patient_id))
        context = patient.case
        res = requests.post(f'http://{qa_svce_host}:{qa_svce_port}/qa', json={"context":context, "question":question})

        if res.ok:
            answer = res.json()["answer"]
            print(answer)
            return jsonify({"message": f"{answer}"})
        else:
            return jsonify({"message": "Request failed"})
    else:
        return jsonify({"message": "Error authentication failed!"})

@app.route('/patient/<patient_id>', methods=['GET'])
def patient(patient_id):
    if session.get("logged_in"):
        user = helpers.get_user()
        patient = helpers.get_patient(int(patient_id))
        if patient.free or user.paid:
            return render_template('chat.html', user=user, patient=patient)
        else:
            return render_template('home.html', user=user, patients=helpers.get_patients())
    else:
        return redirect(url_for("login"))

# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=os.environ["PORT"], host='0.0.0.0')
