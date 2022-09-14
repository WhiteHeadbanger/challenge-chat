from flask import Blueprint

from src.controllers.room_controller import create_room, show_room_messages, invite_room, send_message_to_room

room_bp = Blueprint('room_bp', __name__)

room_bp.route('/room', methods=['GET'])(show_room_messages)
room_bp.route('/room/create', methods=['POST'])(create_room)
room_bp.route('/room/invite', methods=['POST'])(invite_room)
room_bp.route('/room/send', methods=['POST'])(send_message_to_room)

