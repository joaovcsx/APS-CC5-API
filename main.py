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
import jwt
app = Flask(__name__)
cors = CORS(app)

# cred = credentials.Certificate("dataBase/aps-cc5-communication-firebase-adminsdk-leq9b-786bf404c3.json")
# firebase_admin.initialize_app(cred, { "projectId": "aps-cc5-communication" })
# db = firestore.client()

# chats = db.collection(u'users/5LfHosQOQunkZI7sarqN/chats').document(u'Jonsonsadasdsa')
# chats.set({
#     "user": 'Jones',
#     "msg": "lil mama"
# })
# chats.set({
#     "user2": 'Bretanhe',
#     "msg": "brabo"
# })

# docs = users_ref.stream()
# docs = users_ref.get()
# for doc in docs:
#     print(u'{} => {}'.format(doc.id, doc.to_dict()))

# print(SERVER_TIMESTAMP)
# print(datetime.datetime.now())
# print(FirebaseUserModule.createChat('sdadsadsa', {'user_1': 'jonson', 'user_2': 'kkk'}))
# print(FirebaseUserModule.getTokenChats())
# FirebaseUserModule.test()

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
    print(request.method)
    if request.method == 'GET':
        return ChatModule.check_and_create_chat(request.headers)

if __name__ == '__main__':
    app.run(port=8080)

# Token user jwt
# encoded_jwt = jwt.encode({'user': 'joao', 'user2': 'lu'}, 'secretX', algorithm='HS256')
# print(encoded_jwt)
# print(jwt.decode(encoded_jwt, 'secretX', algorithms=['HS256']))

# sorted
# users = ['lu', 'joao']
# users = sorted(users)
# print(users)