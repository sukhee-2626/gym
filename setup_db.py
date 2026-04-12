"""Setup database with tables + seed data"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User, MembershipPlan, Streak, Exercise
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

    # Seed exercises with YouTube links and goal tags
    exercises = [
        # Weight Loss exercises
        Exercise(name='Jumping Jacks', muscle_group='cardio', equipment='bodyweight', difficulty='beginner',
                 calories_per_min=9, description='Classic full-body cardio warm-up exercise.',
                 youtube_url='https://www.youtube.com/watch?v=iSSAk4XCsRA',
                 goal_tag='weight_loss', sets_recommended=3, reps_recommended='30', rest_seconds=30),
        Exercise(name='Burpees', muscle_group='cardio', equipment='bodyweight', difficulty='intermediate',
                 calories_per_min=11, description='High-intensity full-body exercise for fat burning.',
                 youtube_url='https://www.youtube.com/watch?v=818q1VJuRkc',
                 goal_tag='weight_loss', sets_recommended=3, reps_recommended='10', rest_seconds=45),
        Exercise(name='Mountain Climbers', muscle_group='core', equipment='bodyweight', difficulty='beginner',
                 calories_per_min=9, description='Cardio + core exercise for total fat burn.',
                 youtube_url='https://www.youtube.com/watch?v=nmwgirgXLYM',
                 goal_tag='weight_loss', sets_recommended=3, reps_recommended='20', rest_seconds=30),
        Exercise(name='High Knees', muscle_group='cardio', equipment='bodyweight', difficulty='beginner',
                 calories_per_min=8, description='Fast-paced cardio to spike heart rate.',
                 youtube_url='https://www.youtube.com/watch?v=oDdkytliOqE',
                 goal_tag='weight_loss', sets_recommended=4, reps_recommended='30s', rest_seconds=20),
        Exercise(name='Jump Squats', muscle_group='legs', equipment='bodyweight', difficulty='intermediate',
                 calories_per_min=8, description='Explosive lower body cardio exercise.',
                 youtube_url='https://www.youtube.com/watch?v=CVaEhXotL7M',
                 goal_tag='weight_loss', sets_recommended=3, reps_recommended='15', rest_seconds=45),

        # Muscle Gain exercises
        Exercise(name='Bench Press', muscle_group='chest', equipment='barbell', difficulty='intermediate',
                 calories_per_min=5, description='Primary compound chest exercise for mass.',
                 youtube_url='https://www.youtube.com/watch?v=rT7DgCr-3pg',
                 goal_tag='gain_muscle', sets_recommended=4, reps_recommended='8-10', rest_seconds=90),
        Exercise(name='Pull-ups', muscle_group='back', equipment='bodyweight', difficulty='intermediate',
                 calories_per_min=5, description='Best bodyweight exercise for back width.',
                 youtube_url='https://www.youtube.com/watch?v=eGo4IYlbE5g',
                 goal_tag='gain_muscle', sets_recommended=4, reps_recommended='8', rest_seconds=90),
        Exercise(name='Barbell Squat', muscle_group='legs', equipment='barbell', difficulty='intermediate',
                 calories_per_min=6, description='King of all exercises. Builds overall mass.',
                 youtube_url='https://www.youtube.com/watch?v=bEv6CCg2BC8',
                 goal_tag='gain_muscle', sets_recommended=4, reps_recommended='8-10', rest_seconds=120),
        Exercise(name='Deadlift', muscle_group='back', equipment='barbell', difficulty='advanced',
                 calories_per_min=6, description='Total body strength builder.',
                 youtube_url='https://www.youtube.com/watch?v=op9kVnSso6Q',
                 goal_tag='gain_muscle', sets_recommended=4, reps_recommended='6', rest_seconds=120),
        Exercise(name='Overhead Press', muscle_group='shoulders', equipment='barbell', difficulty='intermediate',
                 calories_per_min=5, description='Builds shoulder size and upper body strength.',
                 youtube_url='https://www.youtube.com/watch?v=2yjwXTZQDDI',
                 goal_tag='gain_muscle', sets_recommended=3, reps_recommended='10', rest_seconds=90),

        # Maintenance exercises
        Exercise(name='Push-ups', muscle_group='chest', equipment='bodyweight', difficulty='beginner',
                 calories_per_min=4, description='Classic upper body exercise. Great for maintenance.',
                 youtube_url='https://www.youtube.com/watch?v=IODxDxX7oi4',
                 goal_tag='maintain', sets_recommended=3, reps_recommended='12', rest_seconds=60),
        Exercise(name='Plank', muscle_group='core', equipment='bodyweight', difficulty='beginner',
                 calories_per_min=3, description='Core stability and endurance exercise.',
                 youtube_url='https://www.youtube.com/watch?v=ASdvN_XEl_c',
                 goal_tag='maintain', sets_recommended=3, reps_recommended='45s', rest_seconds=30),
        Exercise(name='Lunges', muscle_group='legs', equipment='bodyweight', difficulty='beginner',
                 calories_per_min=5, description='Lower body compound exercise for balance and strength.',
                 youtube_url='https://www.youtube.com/watch?v=QOVaHwm-Q6U',
                 goal_tag='maintain', sets_recommended=3, reps_recommended='12 each', rest_seconds=45),
        Exercise(name='Dumbbell Row', muscle_group='back', equipment='dumbbell', difficulty='beginner',
                 calories_per_min=4, description='Unilateral back exercise for posture and muscle balance.',
                 youtube_url='https://www.youtube.com/watch?v=roCP6wCXPqo',
                 goal_tag='maintain', sets_recommended=3, reps_recommended='12', rest_seconds=60),
    ]
    for ex in exercises:
        db.session.add(ex)

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

    # Seed admin user
    admin = User(
        name='Admin', email='admin@smartgym.ai',
        phone='8888888888', gender='male', age=30,
        weight_kg=70, height_cm=175,
        goal='maintain', fitness_level='intermediate',
        role='admin', daily_budget=300, qr_token=str(uuid.uuid4()),
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.flush()
    admin_streak = Streak(user_id=admin.id)
    db.session.add(admin_streak)

    db.session.commit()
    print("[OK] Database created!")
    print("    Member login: demo@smartgym.ai / demo123")
    print("    Admin login:  admin@smartgym.ai / admin123")
