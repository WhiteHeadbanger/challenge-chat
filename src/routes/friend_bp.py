from flask import Blueprint

from src.controllers.friend_controller import send_friend_request, handle_friend_request, delete_friend, show_private_messages, send_private_message

friend_bp = Blueprint('friend_bp', __name__)

friend_bp.route('/friendrequest/send', methods=['POST'])(send_friend_request)
friend_bp.route('/friendrequest/handle', methods=['POST'])(handle_friend_request)
friend_bp.route('/friend/delete', methods=['DELETE'])(delete_friend)
friend_bp.route('/pm', methods=['GET'])(show_private_messages)
friend_bp.route('/pm/send', methods=['POST'])(send_private_message)