from flask import request, session, jsonify

from src.models.user import User
from src.models.chat import Chat

chat = Chat()

def register() -> str:
    if request.method == 'POST':
        username = request.args['username']
        if not chat.user_exists(username):
            # Create user
            chat.add_user(User(nickname=username))

            result_data = {
                'success': True,
                'data': f"{username} registered."
            }
        else:
            result_data = {
                'success': False,
                'data': f"{username} already exists."
            }

        return jsonify(result_data), 200

def login() -> str:
    if request.method == 'POST':
        username = request.args['username']
        if chat.user_exists(username):
            if session.get('username') is not None:
                
                result_data = {
                    'success': False,
                    'data': f"{username} is already logged in."
                }
            else:
                session['username'] = username
                
                result_data = {
                    'success': True,
                    'data': f"{username} successfully logged in."
                }
        else:
            result_data = {
                'success': False,
                'data': f"{username} does not exist."
            }

        return jsonify(result_data), 200

def logout() -> str:
    if request.method == 'GET':
        if session.get('username') is not None:
            session.clear()
            
            result_data = {
                'success': True,
                'data': "Successfully logged out."
            }
        else:
            result_data = {
                'success': False,
                'data': "You must first log in." 
            }

        return jsonify(result_data), 200

def delete_account() -> str:
    if request.method == 'DELETE':
        if session.get('username') is not None:
            if chat.user_exists(session.get('username')):
                user = chat.get_user(session.get('username'))
                chat.remove_user(user)
                """ chat.nicknames.remove(session.get('username'))
                chat.users.remove(chat.get_user(session.get('username'))) """
                session.clear()
                
                result_data = {
                    'success': True,
                    'data': f"Account deleted."
                }
            else:
                result_data = {
                    'success': False,
                    'data': f"{chat.get_user(session.get('username')).nickname} does not exist."
                }

        return jsonify(result_data), 200