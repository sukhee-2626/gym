"""Workout Routes - Goal-based exercises from DB, log session, history"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import UserWorkout, Streak, Notification, Exercise
from app.ai_engine import get_today_workout, generate_workout_plan
from datetime import date

workout_bp = Blueprint('workout', __name__)


@workout_bp.route('/')
@login_required
def index():
    # Get AI weekly plan (structure/schedule)
    weekly_plan = generate_workout_plan(current_user.goal, current_user.fitness_level)
    today_plan = get_today_workout(current_user.goal, current_user.fitness_level)

    # Get goal-based exercises from DB (admin-customizable)
    goal_map = {
        'lose_weight': 'weight_loss',
        'weight_loss': 'weight_loss',
        'gain_muscle': 'gain_muscle',
        'maintain': 'maintain',
        'maintenance': 'maintain',
        'endurance': 'weight_loss',  # cardio-heavy
    }
    goal_tag = goal_map.get(current_user.goal, 'maintain')
    db_exercises = Exercise.query.filter(
        db.or_(
            Exercise.goal_tag == goal_tag,
            Exercise.goal_tag == 'all'
        ),
        Exercise.is_active == True
    ).all()

    history = UserWorkout.query.filter_by(
        user_id=current_user.id
    ).order_by(UserWorkout.date.desc()).limit(10).all()

    return render_template('workout/index.html',
        weekly_plan=weekly_plan,
        today_plan=today_plan,
        db_exercises=db_exercises,
        history=history,
    )


@workout_bp.route('/log', methods=['POST'])
@login_required
def log_workout():
    today = date.today()
    existing = UserWorkout.query.filter_by(user_id=current_user.id, date=today).first()
    if not existing:
        workout = UserWorkout(
            user_id=current_user.id,
            duration_mins=int(request.form.get('duration', 30)),
            calories_burned=float(request.form.get('calories', 0)),
            notes=request.form.get('notes', ''),
        )
        db.session.add(workout)

        streak = current_user.streaks
        if streak:
            from datetime import timedelta
            last = streak.last_workout_date
            yesterday = today - timedelta(days=1)
            if last == yesterday:
                streak.workout_streak += 1
            elif last != today:
                streak.workout_streak = 1
            streak.last_workout_date = today
            streak.max_workout_streak = max(streak.workout_streak, streak.max_workout_streak)
            streak.total_points += 10
        db.session.commit()
        flash('Workout logged! Great job! 💪', 'success')
    else:
        flash('Already logged a workout today!', 'error')
    return redirect(url_for('workout.index'))


@workout_bp.route('/api/plan')
@login_required
def api_plan():
    plan = generate_workout_plan(current_user.goal, current_user.fitness_level)
    return jsonify(plan)
