# coding: utf-8
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from class_util import UserModule 
from class_util import ChatModule
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin.firestore import SERVER_TIMESTAMP
import datetime
from firebase_module import FirebaseUserModule
from firebase_module import FirebaseChatModule
import jwt
app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def hello_world():
    return 'API do João!'

@app.route('/user', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return UserModule.getUser()

    if request.method == 'POST':
        return UserModule.createUser(request.json)

@app.route('/user-chats', methods=['GET', 'POST'])
def chats():
    if request.method == 'GET':
        return ChatModule.check_and_create_chat(request.headers)
    if request.method == 'POST':
        return ChatModule.notify_message_sending(request.json)

if __name__ == '__main__':
    app.run(port=8050)

