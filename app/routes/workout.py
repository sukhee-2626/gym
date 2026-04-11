"""Workout Routes - AI plan, log session, history"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import UserWorkout, Streak, Notification
from app.ai_engine import generate_workout_plan, get_today_workout, calculate_calories_burned
from datetime import date

workout_bp = Blueprint('workout', __name__)


@workout_bp.route('/')
@login_required
def index():
    plan = generate_workout_plan(current_user.goal, current_user.fitness_level)
    today_plan = get_today_workout(current_user.goal, current_user.fitness_level)
    history = UserWorkout.query.filter_by(
        user_id=current_user.id
    ).order_by(UserWorkout.date.desc()).limit(10).all()
    return render_template('workout/index.html',
        weekly_plan=plan,
        today_plan=today_plan,
        history=history,
    )


@workout_bp.route('/log', methods=['POST'])
@login_required
def log_workout():
    data = request.get_json()
    duration = int(data.get('duration', 30))
    exercises = data.get('exercises', [])
    cal_burned = calculate_calories_burned(exercises, current_user.weight_kg or 70)

    # Check if already logged today
    existing = UserWorkout.query.filter_by(
        user_id=current_user.id, date=date.today()
    ).first()

    if not existing:
        workout = UserWorkout(
            user_id=current_user.id,
            duration_mins=duration,
            calories_burned=cal_burned,
            notes=data.get('notes', ''),
        )
        db.session.add(workout)

        # Update streak
        streak = current_user.streaks
        if streak:
            last = streak.last_workout_date
            if last == date.today() - __import__('datetime').timedelta(days=1):
                streak.workout_streak += 1
            elif last != date.today():
                streak.workout_streak = 1
            streak.last_workout_date = date.today()
            streak.max_workout_streak = max(streak.workout_streak, streak.max_workout_streak)
            streak.total_points += 10

        db.session.commit()
        return jsonify({"success": True, "calories_burned": cal_burned, "streak": streak.workout_streak if streak else 1})

    return jsonify({"success": False, "message": "Already logged today!"})


@workout_bp.route('/api/plan')
@login_required
def api_plan():
    plan = generate_workout_plan(current_user.goal, current_user.fitness_level)
    return jsonify(plan)
