from flask import request, session, jsonify
import json

from src.models.chat import Chat

chat = Chat()

def send_friend_request():
    if request.method == 'POST':
        username = request.args['username']
        if session.get('username') is not None:
            current_user = chat.get_user(session.get('username'))
            if current_user is not None:
                to_user = chat.get_user(username)
                if to_user is not None:
                    data = {
                        'type': 'friend_request',
                        'from': session.get('username')
                    }
                    to_user.receive_friend_request(data)

                    result_data = {
                        'success': True,
                        'data': f"Friend request sent to {username}",
                    }
                else:
                    result_data = {
                        'success': False,
                        'data': f"{username} not found."
                    }
            else:
                result_data = {
                    'success': False,
                    'data': "You are not logged in."
                }
        else:
            result_data = {
                    'success': False,
                    'data': f"You are not logged in.",
                }

        return jsonify(result_data), 200

def handle_friend_request():
    if request.method == 'POST':
        username = request.args['username']
        friend_request = request.args['accept']
        current_user = chat.get_user(session.get('username'))
        if current_user is not None:
            from_user = chat.get_user(username)
            
            f_req = None
            for req in current_user.friend_requests:
                if req['from'] == from_user.nickname:
                    f_req = req

            if f_req is not None:
                # if accepted
                if friend_request == 'true':
                    current_user.add_friend(username)
                    from_user.add_friend(current_user.nickname)
                    
                    result_data = {
                        'success': True,
                        'data': f"Accepted {username}'s friend request."
                    }
                else:
                    result_data = {
                        'success': True,
                        'data': f"Denied {username}'s friend request"
                    }
                
                # Accepted or denied, the request must be removed.
                friend_request_list = [req for req in current_user.friend_requests if req['from'] != from_user.nickname]
                current_user.friend_requests = friend_request_list
        else:
            result_data = {
                'success': False,
                'data': "You are not logged in."
            }

        return jsonify(result_data), 200

def delete_friend():
    if request.method == 'DELETE':
        username = request.args['username']

        if session.get('username') is not None:
            current_user = chat.get_user(session.get('username'))
            if current_user is not None:
                to_user = chat.get_user(username)

                if to_user is not None:
                    if current_user.in_friendlist(to_user.nickname):
                        current_user.remove_friend(username)
                        to_user.remove_friend(session.get('username'))

                        result_data = {
                            'success': True,
                            'data': f"{username} removed from friend list."
                        }
                    else:
                        result_data = {
                            'success': False,
                            'data': f"{username} is not your friend."
                        }
                else:
                    result_data = {
                        'success': False,
                        'data': f"{username} not found."
                    }
            else:
                result_data = {
                    'success': False,
                    'data': "You are not logged in."
                }
        else:
            result_data = {
                'success': False,
                'data': "You are not logged in."
            }

        return jsonify(result_data), 200

def show_private_messages():
    if request.method == 'GET':
        if session.get('username') is not None:
            current_user = chat.get_user(session.get('username'))
            
            if current_user is not None:
                data = current_user.get_private_messages()
                
                result_data = {
                    'success': True,
                    'data': data
                }
            else:
                result_data = {
                'success': False,
                'data': 'You are not logged in.'
            }
        else:
            result_data = {
                'success': False,
                'data': 'You are not logged in.'
            }
    
        return jsonify(result_data), 200

def send_private_message():
    if request.method == 'POST':
        username = request.args['username']
        message = request.args['message']

        if session.get('username') is not None:
            current_user = chat.get_user(session.get('username'))
            
            if current_user is not None:
                if current_user.in_friendlist(username):
                    to_user = chat.get_user(username)
                    if to_user is not None:
                        data = {
                            'type': 'private_message',
                            'from': session.get('username'),
                            'to': username,
                            'message': message
                        }
                        current_user.messages.append(data)
                        to_user.messages.append(data)
                        
                        result_data = {
                            'success': True,
                            'data': data
                        }

                else:
                    result_data = {
                        'success': False,
                        'data': f"{username} is not your friend."
                    }
            else:
                result_data = {
                    'success': False,
                    'data': "You are not logged in."
                }
        else:
            result_data = {
                'success': False,
                'data': "You are not logged in."
            }

        return jsonify(result_data), 200