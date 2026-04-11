"""Setup database with tables + seed data"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User, MembershipPlan, Streak
import uuid

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Seed membership plans
    plans = [
        MembershipPlan(name='Basic',    duration_days=30,  price=799,  features='AI Workout Plans,Diet Planner,Calorie Tracker,Attendance Tracking'),
        MembershipPlan(name='Pro',      duration_days=90,  price=1999, features='All Basic Features,Progress Analytics,Streak Rewards,Priority Support'),
        MembershipPlan(name='Elite',    duration_days=365, price=5999, features='All Pro Features,Personal Coach Access,Nutrition Consultation,Custom Plans'),
    ]
    for p in plans:
        db.session.add(p)

    # Seed demo user
    demo = User(
        name='Demo User', email='demo@smartgym.ai',
        phone='9999999999', gender='male', age=25,
        weight_kg=75, height_cm=175,
        goal='gain_muscle', fitness_level='beginner',
        daily_budget=200, qr_token=str(uuid.uuid4()),
    )
    demo.set_password('demo123')
    db.session.add(demo)
    db.session.flush()

    streak = Streak(user_id=demo.id, workout_streak=5, attendance_streak=3,
                    max_workout_streak=5, total_points=120)
    db.session.add(streak)

    db.session.commit()
    print("[OK] Database created with plans + demo user!")
    print("   Login: demo@smartgym.ai / demo123")
