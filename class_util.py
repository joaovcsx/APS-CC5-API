from firebase_module import FirebaseUserModule
import jwt

class User:
    # def __init__(self):
    #     self.name
    #     self.password 

    @staticmethod
    def getUser():
        users = FirebaseUserModule.getNameUsers()
        return users
        
    @staticmethod
    def createUser(user):
        return '%s' % FirebaseUserModule.createUser(user)

    @staticmethod
    def check_user_authentication(headers):
        """
            Check user authentication
            :param User user: User
            :return str msg|token: string
        """
        db_users = FirebaseUserModule.getUsers()
        for check_user in db_users:
            if check_user['login'] == headers['login']:
                if check_user['password'] == headers['password']:
                    return check_user['token']
                else:
                    return 'user invalid'
        return 'user invalid'

    @staticmethod
    def check_and_create_chat(headers):
        if not checkIfUserExist(
            headers['user_2'], FirebaseUserModule.getNameUsers()):
            return {'error': 'User "%s" not exists' % headers['user_2']}
        
        db_chats = FirebaseUserModule.getTokenChats()
        if db_chats:
            for chat in db_chats:
                if headers['user_1'] in [chat['user_1'], chat['user_2']] and (
                    headers['user_2'] in [chat['user_1'], chat['user_2']]
                    ):
                        return {
                            'status': 'alread created',
                            'chat': chat['chat']
                        }
        token_chat = jwt.encode(
            {'user_1': headers['user_1'], 'user_2': headers['user_2']}, 'secretX', algorithm='HS256').split('.')[1]
        return FirebaseUserModule.createChat(token_chat, headers)
        # db_chats = open('dataBase/chats.txt', 'a')
        # db_chats.writelines('\n{}"/"-{}"/"-{}'.format(headers['name_1'], 
        #     headers['name_2'], token_chat))
        # return {'action': 'create', 'chat': token_chat }

def checkIfUserExist(name, users_name):
    if users_name:
        if name in users_name:
            return True
        else:
            return False
    else:
        return False