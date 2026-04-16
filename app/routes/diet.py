"""Diet Routes - AI meal plan + food logging"""
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import FoodEntry, Streak
from app.ai_engine import generate_diet_plan, INDIAN_FOOD_DB
from datetime import date

diet_bp = Blueprint('diet', __name__)


@diet_bp.route('/')
@login_required
def index():
    plan = generate_diet_plan(
        goal=current_user.goal,
        tdee=current_user.tdee,
        budget_inr=current_user.daily_budget,
        is_veg=True  # MVP default; can be user preference
    )
    today_entries = FoodEntry.query.filter_by(
        user_id=current_user.id, date=date.today()
    ).all()
    total_cals = sum(e.calories for e in today_entries)
    total_protein = sum(e.protein_g for e in today_entries)
    total_cost = sum(e.cost_inr for e in today_entries)
    return render_template('diet/index.html',
        plan=plan,
        today_entries=today_entries,
        total_cals=round(total_cals),
        total_protein=round(total_protein, 1),
        total_cost=round(total_cost),
        food_db=INDIAN_FOOD_DB,
        goal=current_user.goal,
        tdee=current_user.tdee,
    )


@diet_bp.route('/log', methods=['POST'])
@login_required
def log_food():
    # Accept both form POST and JSON
    if request.is_json:
        data = request.get_json()
        food_name = data.get('food_name')
        meal_type = data.get('meal_type', 'snack')
        use_json = True
    else:
        food_name = request.form.get('food_name')
        meal_type = request.form.get('meal_type', 'snack')
        use_json = False

    if food_name and food_name in INDIAN_FOOD_DB:
        fd = INDIAN_FOOD_DB[food_name]
        entry = FoodEntry(
            user_id=current_user.id,
            date=date.today(),
            meal_type=meal_type,
            food_name=food_name,
            quantity_g=fd['g'],
            calories=fd['cal'],
            protein_g=fd['protein'],
            carbs_g=fd['carbs'],
            fat_g=fd['fat'],
            cost_inr=fd['cost'],
        )
        db.session.add(entry)

        streak = current_user.streaks
        if streak and streak.last_diet_date != date.today():
            streak.last_diet_date = date.today()
            streak.diet_streak = (streak.diet_streak + 1)
            streak.total_points += 5

        db.session.commit()

        if use_json:
            return jsonify({"success": True, "entry": {
                "food": food_name, "cal": fd['cal'],
                "protein": fd['protein'], "cost": fd['cost']
            }})
        flash(f'✅ {food_name} logged! ({fd["cal"]} kcal)', 'success')
        return redirect(url_for('diet.index'))

    if use_json:
        return jsonify({"success": False, "message": "Food not found"})
    flash('Food not found. Please select from the list.', 'error')
    return redirect(url_for('diet.index'))


@diet_bp.route('/delete/<int:entry_id>', methods=['DELETE'])
@login_required
def delete_food(entry_id):
    entry = FoodEntry.query.get_or_404(entry_id)
    if entry.user_id == current_user.id:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 403


@diet_bp.route('/api/foods')
@login_required
def api_foods():
    q = request.args.get('q', '').lower()
    results = {k: v for k, v in INDIAN_FOOD_DB.items() if q in k.lower()} if q else INDIAN_FOOD_DB
    return jsonify(results)
