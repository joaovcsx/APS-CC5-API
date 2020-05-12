# coding: utf-8
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from class_util import ChatModule, UserModule
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin.firestore import SERVER_TIMESTAMP
import datetime
from firebase_module import FirebaseChatModule, FirebaseUserModule
import jwt
import os

app = Flask(__name__)
# cors = CORS(app)
cors = CORS(app, resource={r"/*":{"origins": "*"}})

@app.route('/')
def hello_world():
    return 'API - CC5P22'

@app.route('/user', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return UserModule.get_users()

    if request.method == 'POST':
        return UserModule.post_user(request.json)

@app.route('/user-chats', methods=['GET', 'POST'])
def chats():
    if request.method == 'GET':
        return ChatModule.check_and_create_chat(request.headers)
    if request.method == 'POST':
        return ChatModule.notify_message_sending(request.json)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port)
    # app.run(port=8050)

