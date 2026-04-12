"""Dashboard Route - Main hub with stats overview"""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models import Attendance, FoodEntry, UserWorkout, Notification, WeightLog, Membership
from app import db
from datetime import date, timedelta

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/home')
@dashboard_bp.route('/')
@login_required
def index():
    today = date.today()

    # Today's quick stats
    today_food = FoodEntry.query.filter_by(user_id=current_user.id, date=today).all()
    cal_intake = sum(f.calories for f in today_food)

    today_workout = UserWorkout.query.filter_by(user_id=current_user.id, date=today).first()
    cal_burned = today_workout.calories_burned if today_workout else 0

    # Check active membership
    membership = Membership.query.filter_by(
        user_id=current_user.id, status='active'
    ).order_by(Membership.end_date.desc()).first()

    # Recent notifications
    notifications = Notification.query.filter_by(
        user_id=current_user.id, is_read=False
    ).order_by(Notification.created_at.desc()).limit(5).all()

    # Weight progress (last 7 entries)
    weight_logs = WeightLog.query.filter_by(
        user_id=current_user.id
    ).order_by(WeightLog.logged_date.desc()).limit(7).all()
    weight_logs = list(reversed(weight_logs))

    # Weekly attendance (last 7 days)
    week_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    attendance_dates = {
        a.check_in.date()
        for a in Attendance.query.filter_by(user_id=current_user.id).all()
    }
    week_attendance = [d in attendance_dates for d in week_dates]

    return render_template('dashboard/index.html',
        cal_intake=int(cal_intake),
        cal_burned=int(cal_burned or 0),
        cal_target=current_user.tdee,
        membership=membership,
        notifications=notifications,
        weight_logs=weight_logs,
        week_dates=[d.strftime('%a') for d in week_dates],
        week_attendance=week_attendance,
        streak=current_user.streaks,
    )


@dashboard_bp.route('/api/stats')
@login_required
def api_stats():
    """JSON stats for charts"""
    today = date.today()
    # Last 30 days calorie data
    days = [today - timedelta(days=i) for i in range(29, -1, -1)]
    cal_data = []
    for d in days:
        entries = FoodEntry.query.filter_by(user_id=current_user.id, date=d).all()
        cal_data.append(sum(e.calories for e in entries))

    weight_logs = WeightLog.query.filter_by(
        user_id=current_user.id
    ).order_by(WeightLog.logged_date).limit(30).all()

    return jsonify({
        "calories": {
            "labels": [d.strftime('%b %d') for d in days],
            "data": cal_data,
            "target": current_user.tdee,
        },
        "weight": {
            "labels": [w.logged_date.strftime('%b %d') for w in weight_logs],
            "data": [w.weight_kg for w in weight_logs],
        }
    })
