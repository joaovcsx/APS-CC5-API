# coding: utf-8
from firebase_module import FirebaseUserModule 
from firebase_module import FirebaseChatModule 
import jwt
from flask import jsonify

class UserModule:

    @staticmethod
    def get_users():
        return jsonify(FirebaseUserModule.get_email_users())
        
    @staticmethod
    def post_user(request):
        if request['action'] == 'create':
            return jsonify(FirebaseUserModule.create_user(request['user']))
        if request['action'] == 'update':
            response = FirebaseUserModule.update_user(request['user'])
            if response['status'] == 'update':
                return jsonify(response), 201
            if response['status'] == 'error':
                return jsonify(response), 400
        return jsonify({u'erro': u'Bad request'}), 400 
        
class ChatModule:
    @staticmethod
    def check_and_create_chat(params):
        if not check_params_create_chat(params):
            return jsonify({u'erro': u'Bad request'}), 400

        db_chat = FirebaseChatModule.get_conversation_key(
            params['uid'], params['uid_of_user'])
        if db_chat:
            return jsonify({
                'status': 'alread created',
                'chat': db_chat
            }), 200
        token_chat = jwt.encode(
            {
                'user_1': params['my_email'], 
                'user_2': params['email_of_user']
            }, 'secretX', algorithm='HS256').split('.')[1]
        return jsonify(FirebaseChatModule.create_chat(token_chat, params))

    @staticmethod
    def notify_message_sending(params):
        if params['action'] == 'notify':
            response = FirebaseChatModule.notify_message_sending(params)
            if response['status'] == 'executed_successfully':
                return jsonify({u'status': u'notified_with_success'}), 201 
            return jsonify(response), 400
        if params['action'] == 'remove_notify':
            if FirebaseChatModule.remove_notify_message_sending(params):
                return jsonify({u'status': u'removed_notified_with_success'}), 201 
        return jsonify({u'erro': u'Bad request'}), 400 

def check_params_create_chat(params):
    try:
        if params['uid'] and params['my_email'] and ( 
            params['email_of_user'] and params['uid_of_user']
        ):
            users_email = FirebaseUserModule.get_email_users()
            if params['my_email'] in users_email and (
                params['email_of_user'] in users_email
            ):
                return True
        return False
    except:
        return False