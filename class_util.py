# coding: utf-8
from firebase_module import FirebaseUserModule 
from firebase_module import FirebaseChatModule 
import jwt
from flask import jsonify

class UserModule:

    @staticmethod
    def getUser():
        users = jsonify(FirebaseUserModule.getEmailUsers())
        return users
        
    @staticmethod
    def createUser(user):
        return jsonify(FirebaseUserModule.createUser(user))
        
class ChatModule:
    @staticmethod
    def check_and_create_chat(params):
        if not checkParamsCreateUser(params):
             return jsonify({u'erro': u'Bad request'}), 400

        db_chat = FirebaseChatModule.getTokenChat(
            params['uid'], params['uid_of_user'])
        if db_chat:
            return jsonify({
                'status': 'alread created',
                'chat': db_chat
            }), 200
        token_chat = jwt.encode(
            {'user_1': params['my_email'], 
            'user_2': params['email_of_user']}, 
            'secretX', algorithm='HS256'
        ).split('.')[1]
        return jsonify(FirebaseChatModule.createChat(token_chat, params))

    @staticmethod
    def notify_message_sending(params):
        if params['action'] == 'notify':
            if FirebaseChatModule.notify_message_sending(params):
                return jsonify({u'status': u'notified_with_success'}), 201 
        if params['action'] == 'remove_notify':
            if FirebaseChatModule.remove_notify_message_sending(params):
                return jsonify({u'status': u'removed_notified_with_success'}), 201 
        return jsonify({u'erro': u'Bad request'}), 400 

def checkParamsCreateUser(params):
    try:
        if params['uid'] and params['my_email'] and ( 
            params['email_of_user'] and params['uid_of_user']
        ):
            users_email = FirebaseUserModule.getEmailUsers()
            if params['my_email'] in users_email and (
                params['email_of_user'] in users_email
            ):
                return True
        return False
    except:
        return False