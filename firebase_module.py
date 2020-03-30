import firebase_admin
from firebase_admin           import credentials
from firebase_admin           import firestore
import jwt
import json 
from firebase_admin.firestore import SERVER_TIMESTAMP
import datetime

cred = credentials.Certificate("dataBase/aps-cc5-communication-firebase-adminsdk-leq9b-786bf404c3.json")
firebase_admin.initialize_app(cred, { "projectId": "aps-cc5-communication" })
db = firestore.client()

class FirebaseUserModule():

    @staticmethod
    def getNameUsers():
        users = db.collection(u'users').get()
        login_users = []
        for user in users:
            login_users.append(user.to_dict()['login'])
        return login_users

    @staticmethod
    def getUsers():
        users = db.collection(u'users').get()
        login_users = []
        for user in users:
            login_users.append(user.to_dict())
        return login_users

    @staticmethod
    def createUser(user):
        if not checkIfUserExist(user['login']):
            user_token = str(jwt.encode({'login': user['login'], 
                'password': user['password']}, 'secretX', algorithm='HS256'))
            print(type(user_token))
            create_query = db.collection(u'users').document(u'%s' % user_token.split('.')[1])
            obj_parameters = {
                u"login": user['login'],
                u"password": user['password'],
                u"nickname": user['nickname'],
                u"email": user['email'],
                u"token": u'%s' % user_token,
                u"datetime": SERVER_TIMESTAMP
            }
            create_query.set(obj_parameters)
            return {'status': 'user created', 'token': user_token}
        else:
            return {'status': 'user already registered'}

    @staticmethod
    def chats():
        teste = db.collection(u'chats').get()
        te = []
        for test in teste:
            te.append(test.id)
        print(te)
        if teste:
            return True
        else: 
            return False

    @staticmethod
    def createChat(token, headers):
        query_create = db.collection(u'chats/parameters/chat_token').document()
        query_create.set({
            u"user_1": u'%s' % headers['user_1'],
            u"user_2": u'%s' % headers['user_2'],
            u"chat": u'%s' % token,
            u"datetime": SERVER_TIMESTAMP
        })
        return { 'status': 'created', 'chat': token }

    @staticmethod
    def getTokenChats():
        try:
            query_chats = db.collection(u'chats/parameters/chat_token').get()
            chats = []
            for chat in query_chats:
                chats.append(chat.to_dict())
            return chats
        except: 
            return False

def checkIfUserExist(name):
    users = db.collection(u'users').get()
    name_users = []
    if users:
        for user in users:
            name_users.append(user.to_dict()['login'])
        if name in name_users:
            return True
        else:
            return False
    else:
        return False
