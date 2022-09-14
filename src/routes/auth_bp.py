from flask import Blueprint

from src.controllers.auth_controller import register, login, logout, delete_account

auth_bp = Blueprint('auth_bp', __name__)

auth_bp.route('/register', methods=['POST'])(register)
auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/logout', methods=['GET'])(logout)
auth_bp.route('/deleteaccount', methods=['DELETE'])(delete_account)