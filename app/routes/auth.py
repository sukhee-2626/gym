"""Authentication Routes: Register, Login, Logout, Profile Setup"""
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Streak

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        if User.query.filter_by(email=data['email']).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('auth.register'))
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            gender=data.get('gender'),
            age=int(data.get('age', 0)) or None,
            weight_kg=float(data.get('weight', 0)) or None,
            height_cm=float(data.get('height', 0)) or None,
            goal=data.get('goal', 'maintain'),
            fitness_level=data.get('level', 'beginner'),
            daily_budget=float(data.get('budget', 150)),
            qr_token=str(uuid.uuid4()),
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.flush()
        streak = Streak(user_id=user.id)
        db.session.add(streak)
        db.session.commit()
        login_user(user)
        flash('Welcome to SmartGym! 🎉', 'success')
        return redirect(url_for('dashboard.index'))
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.check_password(request.form['password']):
            login_user(user, remember=True)
            return redirect(url_for('dashboard.index'))
        flash('Invalid email or password.', 'error')
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        data = request.form
        current_user.name = data.get('name', current_user.name)
        current_user.phone = data.get('phone', current_user.phone)
        current_user.age = int(data.get('age', 0)) or current_user.age
        current_user.weight_kg = float(data.get('weight', 0)) or current_user.weight_kg
        current_user.height_cm = float(data.get('height', 0)) or current_user.height_cm
        current_user.goal = data.get('goal', current_user.goal)
        current_user.fitness_level = data.get('level', current_user.fitness_level)
        current_user.daily_budget = float(data.get('budget', current_user.daily_budget))
        db.session.commit()
        flash('Profile updated!', 'success')
    return render_template('auth/profile.html', user=current_user)
