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
    def getEmailUsers():
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
                u"token": u'{}'.format(user_token),
                u"datetime": SERVER_TIMESTAMP,   
            }
            create_query.set(parameters_user)
            return {u"status": u"user created", u"token": str(user_token.split('.')[1])}
        except Exception as erro:
            return filter_error_returned_from_firebase(erro)
            #  return {u'erro': u'Bad request'}, 401

    # @staticmethod
    # def test():
        # query_create = db.collection(
        # u'parameters/conversations_to_users/%s' % 'idUsers').document('asdasd')
        # query_create.set({
        #     u"user": u'joaovitor@quickfast.com',
        #     u"viewed": False,
        #     u"chat": u'chat',
        #     u"last_conversation_at": SERVER_TIMESTAMP
        # })
        # # query_create.update({
        # #     u"viewed": False,
        # #     u"last_conversation_at": SERVER_TIMESTAMP
        # # })
        # query_create = db.collection(
        #     u'parameters/conversations_to_users/%s' % 'idUsers').stream()
        # for doc in query_create:
        #     print(u'{} => {}'.format(doc.id, doc.to_dict()))
        # print('gg')

class FirebaseChatModule():

    @staticmethod
    def createChat(token, headers):
        try:
            query = db.collection(
                u'parameters/conversations_of_users/%s' % headers['uid']
                ).document(headers['uid_of_user'])
            name = db.collection(u'users').document(headers['uid_of_user']
                ).get().to_dict()['nickname']
            query.set({
                u"user": headers['email_of_user'],
                u"uid_user": headers['uid_of_user'],
                u"nickname": u'%s' % name,
                u"viewed": False,
                u"chat": u'{}'.format(str(token)),
                u"last_conversation_at": u'pending',
                u"messages_sent": 0
            })

            query = db.collection(
                u'parameters/conversations_of_users/%s' % headers['uid_of_user']).document(
                    headers['uid'])
            name = db.collection(u'users').document(headers['uid']
                ).get().to_dict()['nickname']
            query.set({
                u"user": headers['my_email'],
                u"uid_user": headers['uid'],
                u"nickname": u'%s' % name,
                u"viewed": False,
                u"chat": u'{}'.format(str(token)),
                u"last_conversation_at": u'pending',
                u"messages_sent": 0
            })
            return { 'status': 'created', 'chat': token }
        except Exception as erro:
            return filter_error_returned_from_firebase(erro), 401

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
    def getTokenChat(uid, uid_user_to_conversation):
        # query = db.collection(
        #     u'parameters/conversations_of_users/{}/{}'.format(
        #         uid, uid_user_to_conversation)).stram()
        query = db.collection(
            u'parameters/conversations_of_users/%s' % uid).document(
                '%s' % uid_user_to_conversation).get()
        if query.to_dict() and query.to_dict()['chat']:
            return query.to_dict()['chat']
        else:
            return False
        
        # try:
        #     query_chats = db.collection(u'chats/parameters/chat_token').get()
        #     chats = []
        #     for chat in query_chats:
        #         chats.append(chat.to_dict())
        #     return chats
        # except: 
        #     return False

    @staticmethod
    def notify_message_sending(params):
        print(params)
        # try:
        query_create = db.collection(
            u'parameters/conversations_of_users/%s' % params['uid_another_user']
            ).document(params['uid_user'])
        messages_sent = query_create.get().to_dict()['messages_sent'] + 1
        query_create.update({
            u"viewed": True,
            u"last_conversation_at": SERVER_TIMESTAMP,
            u"messages_sent": int(messages_sent)
        })
        return True
        # except Exception as erro:
        #     return filter_error_returned_from_firebase(erro), 401

    @staticmethod
    def remove_notify_message_sending(params):
        try:
            query_create = db.collection(u'parameters/conversations_of_users/%s'
                % params['uid_user']).document(params['uid_another_user'])
            query_create.update({
                u"viewed": False,
                u"last_conversation_at": SERVER_TIMESTAMP,
                u"messages_sent": int(0)
            })
            return True
        except Exception as erro:
            return filter_error_returned_from_firebase(erro), 401

def filter_error_returned_from_firebase(erro):
    print(type(erro))
    print(erro)
    if str(erro).split(':')[0] == 'Malformed email address string':
        return {u'status': u'error',
            'error': 'format_email_invalid'}
    if str(erro).split(':')[0] == 'Invalid password string. Password must be a string at least 6 characters long.':
        return {u'status': u'error',
            'error': 'password_least_six_characters'}
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