"""Leaderboard Route"""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models import User, Streak
from app import db

leaderboard_bp = Blueprint('leaderboard', __name__)


@leaderboard_bp.route('/')
@login_required
def index():
    top_users = db.session.query(User, Streak).join(
        Streak, Streak.user_id == User.id
    ).order_by(Streak.total_points.desc()).limit(20).all()
    return render_template('leaderboard/index.html',
        top_users=top_users,
        current_user=current_user,
    )


@leaderboard_bp.route('/api')
@login_required
def api():
    top_users = db.session.query(User, Streak).join(
        Streak, Streak.user_id == User.id
    ).order_by(Streak.total_points.desc()).limit(20).all()
    return jsonify([{
        "rank": i + 1,
        "name": u.name,
        "points": s.total_points,
        "workout_streak": s.workout_streak,
        "is_me": u.id == current_user.id,
    } for i, (u, s) in enumerate(top_users)])
