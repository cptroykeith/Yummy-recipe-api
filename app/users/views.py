from flask import Flask, jsonify, request, session
from app.models import User
from . import users
from app import db

@users.route('/api/signup', methods=['POST'])
def signup():
    json_data = request.json
    user = User(first_name = json_data['first_name'],\
                 last_name = json_data['last_name'],\
                 email = json_data['email'],\
                 password = json_data['password'])
    db.session.add(user)
    db.session.commit()
    message = 'Successfully signed up'
    db.session.close()
    return jsonify({'message':message})

@users.route('/api/login', methods = ['POST'])
def login():
    json_data = request.json
    user = User.query.fetch_by(email = json_data['email']).first()
    if user and User.verify_password(json_data['password']):
        session['logged_in'] = True
        status = True
    else:
        status = False
    return jsonify({'message':status})


@users.route('/api/logout', methods = ['POST'])
def logout():
    session.pop('logged_in', None)
    return jsonify({'message':'successfully logged out'})