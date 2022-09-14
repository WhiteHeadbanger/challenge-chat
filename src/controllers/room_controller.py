from flask import request, session, jsonify

from src.models.room import Room
from src.models.chat import Chat

chat = Chat()

def create_room():
    if request.method == 'POST':
        room_name = request.args['room_name']

        if session.get('username') is not None:
            current_user = chat.get_user(session.get('username'))
            if current_user is not None:
                room = Room(name=room_name, creator=session.get('username'))
                room.add_user(session.get('username'))
                current_user.add_group(room_name)
                chat.rooms.append(room)

                result_data = {
                    'success': True,
                    'data': f"{room_name} created."
                }
            else:
                result_data = {
                    'success': False,
                    'data': "You are not logged in."
                }
        else:
            result_data = {
                'success': False,
                'data': f"You are not logged in."
            }

        return jsonify(result_data), 200

def invite_room():
    if request.method == 'POST':
        room_name = request.args['room_name']
        username = request.args['username']

        if session.get('username') is not None:
            current_user = chat.get_user(session.get('username'))
            to_user = chat.get_user(username)
            to_room = chat.get_room(room_name)

            if to_room is not None:
                if to_user is not None:
                    if current_user.in_friendlist(to_user.nickname):
                        to_user.add_group(room_name)
                        to_room.add_user(username)

                        result_data = {
                            'success': True,
                            'data': f"{username} added to {room_name}"
                        }
                    else:
                        result_data = {
                            'success': False,
                            'data': f"{to_user.nickname} is not your friend."
                        }
            else:
                result_data = {
                    'success': False,
                    'data': f"{room_name} does not exist."
                }
        else:
            result_data = {
                'success': False,
                'data': "You are not logged in."
            }

        return jsonify(result_data), 200

def send_message_to_room():
    if request.method == 'POST':
        room_name = request.args['room_name']
        message = request.args['message']

        if session.get('username') is not None:
            current_user = chat.get_user(session.get('username'))
            if current_user is not None:
                if current_user.in_group(room_name):
                    to_room = chat.get_room(room_name)
                    if to_room is not None:
                        data = {
                            'type': 'room_message',
                            'from': session.get('username'),
                            'to': room_name,
                            'message': message
                        }
                        
                        #current_user.messages.append(data)
                        to_room.messages.append(data)
                        
                        result_data = {
                            'success': True,
                            'data': data
                        }
                else:
                    result_data = {
                        'success': False,
                        'data': f"User {current_user.nickname} does not belong to this room."
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

def show_room_messages():
    if request.method == 'GET':
        room_name = request.args['room_name']

        if session.get('username') is not None:
            current_user = chat.get_user(session.get('username'))
            if current_user is not None:
                to_room = chat.get_room(room_name)
                if to_room is not None and current_user.nickname in to_room.user_list:
                    data = to_room.get_messages()
                
                    result_data = {
                        'success': True,
                        'data': data
                    }
                else:
                    result_data = {
                        'success': False,
                        'data': "You don't belong to this room or this room doesn't exist."
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