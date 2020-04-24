# coding: utf-8
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from firebase_admin import exceptions
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
    
    @staticmethod
    def get_email_users():
        """
        Get email from users
        :return: list string
        """
        try:
            users = db.collection(u'users').get()
            login_users = []
            for user in users:
                login_users.append(user.to_dict()['email'])
            return login_users
        except Exception as erro:
            return filter_error_returned_from_firebase(erro)
        
    @staticmethod
    def get_users():
        """
        Get users
        :return: list User
        """
        try:
            users = db.collection(u'users').get()
            login_users = []
            for user in users:
                login_users.append(user.to_dict())
            return login_users
        except Exception as erro:
            return filter_error_returned_from_firebase(erro)

    @staticmethod
    def create_user(user):
        """
        Get users
        :param user: User
        :return: Json { status: string, token: string }
        """
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
            query = db.collection(u'users').document(
                u'%s' % user_token.split('.')[1])
            parameters_user = {
                u"email": user['email'],
                u"password": user['password'],
                u"nickname": user['nickname'],   
                u"phone": user['phone'],                     
                u"token": u'{}'.format(user_token),
                u"datetime": SERVER_TIMESTAMP,   
            }
            query.set(parameters_user)
            return { u"status": u"user created", u"token": str(user_token.split('.')[1])}
        except Exception as erro:
            return filter_error_returned_from_firebase(erro)

class FirebaseChatModule():

    @staticmethod
    def create_chat(token, headers):
        """
        Create key to conversation between users
        :param token: string
        :param headers: { 
                            my_email: string,
                            uid: strin: string,
                            uid_of_user: string,
                            email_of_user: string,
                        }
        :return: Json { status: string, token: string }
        """
        try:
            # Set talk parameters in key from first user
            query = db.collection(
                u'parameters/conversations_of_users/%s' % headers['uid']
                ).document(headers['uid_of_user'])
            name_from_user = db.collection(u'users').document(headers['uid_of_user']
                ).get().to_dict()['nickname']
            query.set({
                u"user": headers['email_of_user'],
                u"uid_user": headers['uid_of_user'],
                u"nickname": u'%s' % name_from_user,
                u"viewed": False,
                u"chat": u'{}'.format(str(token)),
                u"last_conversation_at": u'pending',
                u"messages_sent": 0
            })
            # Set talk parameters in key from second user
            query = db.collection(
                u'parameters/conversations_of_users/%s' % headers['uid_of_user']).document(
                    headers['uid'])
            name_from_user = db.collection(u'users').document(headers['uid']
                ).get().to_dict()['nickname']
            query.set({
                u"user": headers['my_email'],
                u"uid_user": headers['uid'],
                u"nickname": u'%s' % name_from_user,
                u"viewed": False,
                u"chat": u'{}'.format(str(token)),
                u"last_conversation_at": u'pending',
                u"messages_sent": 0
            })
            return { 'status': 'created', 'chat': token }
        except Exception as erro:
            return filter_error_returned_from_firebase(erro), 401

    @staticmethod
    def get_conversation_key(uid, uid_user_to_talk):
        """
        Get talk key between users
        :param uid: string
        :param uid_user_to_talk: string
        :return: chat: string | False
        """
        try:
            query = db.collection(
                u'parameters/conversations_of_users/%s' % uid).document(
                    '%s' % uid_user_to_talk).get()
            if query.to_dict() and query.to_dict()['chat']:
                return query.to_dict()['chat']
            else:
                return False
        except Exception:
            return False

    @staticmethod
    def notify_message_sending(params):
        """
        Notify user when to send message
        :param params: Object {uid_another_user: string, uid_user: string}
        :return: Json {status: string} | {status: string, error: string}
        """
        try:
            query_create = db.collection(
                u'parameters/conversations_of_users/%s' % params['uid_another_user']
                ).document(params['uid_user'])
            messages_sent = query_create.get().to_dict()['messages_sent'] + 1
            query_create.update({
                u"viewed": True,
                u"last_conversation_at": SERVER_TIMESTAMP,
                u"messages_sent": int(messages_sent)
            })
            return {u'status': u'executed_successfully'}
        except Exception as erro:
            return filter_error_returned_from_firebase(erro)

    @staticmethod
    def remove_notify_message_sending(params):
        """
        Remove notification from user when to send message
        :param params: Object {uid_another_user: string, uid_user: string}
        :return: Json {status: string} | {status: string, error: string}
        """
        try:
            query_create = db.collection(u'parameters/conversations_of_users/%s'
                % params['uid_user']).document(params['uid_another_user'])
            query_create.update({
                u"viewed": False,
                u"last_conversation_at": SERVER_TIMESTAMP,
                u"messages_sent": int(0)
            })
            return {u'status': u'executed_successfully'}
        except Exception as erro:
            return filter_error_returned_from_firebase(erro), 401

def filter_error_returned_from_firebase(erro):
    """
        Remove notification from user when to send message
        :param params: Object {uid_another_user: string, uid_user: string}
        :return: Json {status: string} | {status: string, error: string}
        """
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