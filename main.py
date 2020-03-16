# coding: utf-8
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import jwt
app = Flask(__name__)
cors = CORS(app)

neighborhoods = ['Bairros:']

@app.route('/')
def hello_world():
    return 'API do João!'

# @app.route('/contatos', methods=['GET', 'POST'])
# def contacts():
#     if request.method == 'POST':
#         contact = request.json
#         from pprint import pprint
#         print('\n\n=========================')
#         pprint(contact)
#         print('=========================\n\n')
#         return render_template('contact.html', contact=contact)
#         # return "200 OK"
#     elif request.method == 'GET':     
#         contacts = [
#             {
#                 "nome": "Felipe",
#                 "telefone": "11 998878-7894"
#             },
#             {
#                 "nome": "Joao",
#                 "telefone": "11 7777-7894"
#             }        
#         ]
#         return jsonify(contacts)

@app.route('/contatos', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        contact = request.json
        from pprint import pprint
        print('\n\n=========================')
        pprint(contact)
        print('=========================\n\n')
        # return render_template('contact.html', contact=contact)
        return "200 OK"
    elif request.method == 'GET':     
        contacts = [
            {
                "nome": "Felipe",
                "telefone": "11 998878-7894"
            },
            {
                "nome": "Joao",
                "telefone": "11 7777-7894"
            }        
        ]
        return jsonify(contacts)

@app.route('/user', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':  
        user_list = []
        users_db = open('dataBase/users.txt').readlines()
        for c in range(0, len(users_db)):
            user_list.extend([{
                "login": users_db[c].split()[0],
                "password": users_db[c].split()[1]
            }])
        return jsonify(user_list)

    if request.method == 'POST':
        newUser = request.json
        if checkLogin(newUser['login']):
            user_token = jwt.encode({'Login': newUser['login'], 
                'password': newUser['password']}, 'secretX', algorithm='HS256')
            users_db = open('dataBase/users.txt', 'a')
            users_db.writelines("\n{} {} {}".format(newUser['login'], newUser['password'], user_token))
            users_db.close()
            return user_token
        return 'user already registered'
    

def checkLogin(login):
    users_db = open('dataBase/users.txt').readlines()
    for c in range(0, len(users_db)):
        if users_db[c].split()[0] == login:
            print(users_db[c].split()[0])
            return False
    return True
if __name__ == '__main__':
    app.run()

# Token user jwt
# encoded_jwt = jwt.encode({'some': 'payload'}, 'secretX', algorithm='HS256')
# print(encoded_jwt)
# print(jwt.decode(encoded_jwt, 'secretX', algorithms=['HS256']))