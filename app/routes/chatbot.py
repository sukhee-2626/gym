"""AI Chatbot Route"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.ai_engine import chatbot_response

chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/')
@login_required
def index():
    return render_template('chatbot/index.html')


@chatbot_bp.route('/ask', methods=['POST'])
@login_required
def ask():
    data = request.get_json()
    message = data.get('message', '')
    if not message:
        return jsonify({"response": "Please type a message."})
    response = chatbot_response(message)
    return jsonify({"response": response, "user": current_user.name})
