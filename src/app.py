from flask import Flask, jsonify
from flask_session import Session

from src.routes.auth_bp import auth_bp
from src.routes.friend_bp import friend_bp
from src.routes.room_bp import room_bp

app = Flask(__name__)
app.debug = True
app.config['SECRET_TYPE'] = "secret"
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

app.register_blueprint(auth_bp)
app.register_blueprint(friend_bp)
app.register_blueprint(room_bp)

@app.route('/')
def index():
    result_data = {
        'success': True,
        'data': "Online"
    }

    return jsonify(result_data), 200

if __name__ == '__main__':
    app.run()

