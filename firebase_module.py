# coding: utf-8
import firebase_admin
from firebase_admin           import credentials
from firebase_admin           import firestore
from firebase_admin           import auth
from firebase_admin           import exceptions
import jwt
import json 
from firebase_admin.firestore import SERVER_TIMESTAMP
import datetime
import base64
import random
import uuid
from firebase_admin import _auth_utils

cred = credentials.Certificate("dataBase/aps-cc5-communication-firebase-adminsdk-leq9b-786bf404c3.json")
firebase_admin.initialize_app(cred, { "projectId": "aps-cc5-communication" })
db = firestore.client()

class FirebaseUserModule():

    # @staticmethod
    # def test():
        # try:
        #     random_id = str(uuid.uuid4()).lower().replace('-', '')
        #     user = auth.create_user(
        #         uid= random_id,
        #         email="ssss@jonson.net",
        #         display_name='Random User',
        #         email_verified=False,
        #         password='secret',
        #     )
        #     test = auth.get_user(random_id)
        #     print(test.uid)
        #     return jsonify({u'status': u'created_with_success'})
        # except Exception as erro:
        #     #auth.FirebaseAuthError
        #     # print(filter_error_returned_from_firebase(erro))
        #     return jsonify(filter_error_returned_from_firebase(erro))

        # try:
        #     user = auth.get_user('c1d3750a87704626b2ead2f567b18090')
        #     # user = auth.get_user_by_email('joaovitor@quickfast.com')
        #     print(user.password)
        # except Exception as erro:
        #     print(erro)
        #     print(type(erro))
        #     print(filter_error_returned_from_firebase(erro))

        
    
    @staticmethod
    def getNameUsers():
        users = db.collection(u'users').get()
        login_users = []
        for user in users:
            login_users.append(user.to_dict()['email'])
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
        user_token = jwt.encode({'email': user['email'], 
            'password': user['password']}, 'secretX', algorithm='HS256')
        try:
            # save in authentication user 
            responseCreateUser = auth.create_user(
                uid = str(user_token.split('.')[1]),
                email = user['email'],
                display_name = user['nickname'],
                email_verified = False,
                password = user['password'],
            )
            # save in database
            create_query = db.collection(u'users').document(u'%s' % user_token.split('.')[1])
            parameters_user = {
                u"email": user['email'],
                u"password": user['password'],
                u"nickname": user['nickname'],   
                u"phone": user['phone'],                     
                u"token": user_token,
                u"datetime": SERVER_TIMESTAMP,   
            }
            create_query.set(parameters_user)
            return {u"status": u"user created", u"token": user_token}
        except Exception as erro:
            return filter_error_returned_from_firebase(erro)

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
        query_create = db.collection(
            u'chats/parameters/chat_token').document()
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


# def checkIfUserExist(name):
#     users = db.collection(u'users').get()
#     name_users = []
#     if users:
#         for user in users:
#             name_users.append(user.to_dict()['login'])
#         if name in name_users:
#             return True
#         else:
#             return False
#     else:
#         return False

def filter_error_returned_from_firebase(erro):
    print(type(erro))
    print(erro)
    if type(erro) == _auth_utils.EmailAlreadyExistsError:
        return {u'status': u'error',
            'error': 'user_alread_created'}
    if type(erro) == _auth_utils.UidAlreadyExistsError:
        return {u'status': u'error',
            'error': 'user_alread_created'}
    elif type(erro) == _auth_utils.InvalidIdTokenError:
        return {u'status': u'error',
            u'error': u'user_not_found'}
    elif type(erro) == _auth_utils.UserNotFoundError:
        return {u'status': u'error',
            u'error': u'user_not_exists'}
    elif type(erro) == _auth_utils.UnexpectedResponseError:
        return {u'status': u'error',
            u'error': u'error_request_firebase'}
    elif type(erro) == firebase_admin.exceptions.UnknownError:
        return {u'status': u'error',
            u'error': u'error_request_firebase'}
    elif type(erro) == ValueError :
        return {u'status': u'error',
            u'error': str(erro)}
    else:
        return {u'status': u'error',
            u'error': str(erro)}  

#     test = auth.get_user(random_id)