"""Calorie Tracker + Weight Log Routes"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import FoodEntry, UserWorkout, WeightLog
from datetime import date, timedelta

tracker_bp = Blueprint('tracker', __name__)


@tracker_bp.route('/')
@login_required
def index():
    today = date.today()
    food_entries = FoodEntry.query.filter_by(user_id=current_user.id, date=today).all()
    workout = UserWorkout.query.filter_by(user_id=current_user.id, date=today).first()

    cal_intake = sum(e.calories for e in food_entries)
    cal_burned = workout.calories_burned if workout else 0
    cal_net = cal_intake - cal_burned

    weight_logs = WeightLog.query.filter_by(
        user_id=current_user.id
    ).order_by(WeightLog.logged_date.desc()).limit(10).all()

    macros = {
        "protein": round(sum(e.protein_g for e in food_entries), 1),
        "carbs": round(sum(e.carbs_g for e in food_entries), 1),
        "fat": round(sum(e.fat_g for e in food_entries), 1),
    }

    return render_template('tracker/index.html',
        food_entries=food_entries,
        cal_intake=int(cal_intake),
        cal_burned=int(cal_burned),
        cal_net=int(cal_net),
        cal_target=current_user.tdee,
        macros=macros,
        weight_logs=weight_logs,
    )


@tracker_bp.route('/log-weight', methods=['POST'])
@login_required
def log_weight():
    try:
        weight = float(request.form.get('weight_kg', '') or 0)
    except (ValueError, TypeError):
        weight = 0

    if not weight:
        from flask import flash, redirect, url_for
        flash('Please enter a valid weight.', 'error')
        return redirect(url_for('tracker.index'))

    existing = WeightLog.query.filter_by(
        user_id=current_user.id, logged_date=date.today()
    ).first()

    if existing:
        existing.weight_kg = weight
    else:
        log = WeightLog(
            user_id=current_user.id,
            weight_kg=weight,
            notes=request.form.get('notes', ''),
        )
        db.session.add(log)

    # Always keep user's current weight in sync
    current_user.weight_kg = weight
    db.session.commit()

    from flask import flash, redirect, url_for
    flash(f'Weight logged: {weight} kg ✅', 'success')
    return redirect(url_for('tracker.index'))


@tracker_bp.route('/api/weekly')
@login_required
def weekly_summary():
    today = date.today()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    result = []
    for d in days:
        entries = FoodEntry.query.filter_by(user_id=current_user.id, date=d).all()
        workout = UserWorkout.query.filter_by(user_id=current_user.id, date=d).first()
        result.append({
            "date": d.strftime('%a'),
            "intake": int(sum(e.calories for e in entries)),
            "burned": int(workout.calories_burned if workout else 0),
        })
    return jsonify(result)
