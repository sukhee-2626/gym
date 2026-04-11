"""
SQLAlchemy Database Models - Complete Schema
Tables: User, MembershipPlan, Membership, WorkoutPlan, Exercise,
        UserWorkout, Attendance, DietPlan, FoodEntry, Streak, Notification
"""
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ─────────────────────────────────────────────
#  USER
# ─────────────────────────────────────────────
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(100), nullable=False)
    email          = db.Column(db.String(150), unique=True, nullable=False)
    phone          = db.Column(db.String(15))
    password_hash  = db.Column(db.String(256), nullable=False)
    role           = db.Column(db.String(20), default='member')   # member | admin
    gender         = db.Column(db.String(10))
    age            = db.Column(db.Integer)
    weight_kg      = db.Column(db.Float)
    height_cm      = db.Column(db.Float)
    goal           = db.Column(db.String(50))   # lose_weight | gain_muscle | maintain | endurance
    fitness_level  = db.Column(db.String(20))   # beginner | intermediate | advanced
    daily_budget   = db.Column(db.Float, default=150.0)   # INR for food
    avatar         = db.Column(db.String(200), default='default.png')
    qr_token       = db.Column(db.String(100), unique=True)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    is_active      = db.Column(db.Boolean, default=True)

    # Relationships
    memberships    = db.relationship('Membership', backref='user', lazy=True)
    attendances    = db.relationship('Attendance', backref='user', lazy=True)
    food_entries   = db.relationship('FoodEntry', backref='user', lazy=True)
    streaks        = db.relationship('Streak', backref='user', lazy=True, uselist=False)
    notifications  = db.relationship('Notification', backref='user', lazy=True)
    user_workouts  = db.relationship('UserWorkout', backref='user', lazy=True)
    weight_logs    = db.relationship('WeightLog', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def bmi(self):
        if self.weight_kg and self.height_cm:
            h = self.height_cm / 100
            return round(self.weight_kg / (h * h), 1)
        return None

    @property
    def tdee(self):
        """Total Daily Energy Expenditure (Mifflin-St Jeor)"""
        if not (self.weight_kg and self.height_cm and self.age):
            return 2000
        if self.gender == 'male':
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age + 5
        else:
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age - 161
        multipliers = {'beginner': 1.375, 'intermediate': 1.55, 'advanced': 1.725}
        return int(bmr * multipliers.get(self.fitness_level or 'beginner', 1.375))

    def __repr__(self):
        return f'<User {self.name}>'


# ─────────────────────────────────────────────
#  MEMBERSHIP
# ─────────────────────────────────────────────
class MembershipPlan(db.Model):
    __tablename__ = 'membership_plans'

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)   # Basic | Pro | Elite
    duration_days= db.Column(db.Integer, nullable=False)       # 30, 90, 180, 365
    price        = db.Column(db.Float, nullable=False)         # INR
    features     = db.Column(db.Text)                          # JSON list of features
    is_active    = db.Column(db.Boolean, default=True)

    memberships  = db.relationship('Membership', backref='plan', lazy=True)


class Membership(db.Model):
    __tablename__ = 'memberships'

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_id      = db.Column(db.Integer, db.ForeignKey('membership_plans.id'), nullable=False)
    start_date   = db.Column(db.Date, nullable=False, default=date.today)
    end_date     = db.Column(db.Date, nullable=False)
    amount_paid  = db.Column(db.Float)
    payment_mode = db.Column(db.String(50))   # cash | upi | card
    status       = db.Column(db.String(20), default='active')  # active | expired | pending
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def days_remaining(self):
        delta = self.end_date - date.today()
        return max(0, delta.days)

    @property
    def is_valid(self):
        return self.status == 'active' and self.end_date >= date.today()


# ─────────────────────────────────────────────
#  WORKOUT
# ─────────────────────────────────────────────
class Exercise(db.Model):
    __tablename__ = 'exercises'

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(100), nullable=False)
    muscle_group   = db.Column(db.String(50))   # chest | back | legs | shoulders | arms | core | cardio
    equipment      = db.Column(db.String(50))   # bodyweight | dumbbell | barbell | machine | none
    difficulty     = db.Column(db.String(20))   # beginner | intermediate | advanced
    calories_per_min= db.Column(db.Float, default=5.0)
    description    = db.Column(db.Text)
    video_url      = db.Column(db.String(200))


class WorkoutPlan(db.Model):
    __tablename__ = 'workout_plans'

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # null = template
    name         = db.Column(db.String(100))
    goal         = db.Column(db.String(50))
    level        = db.Column(db.String(20))
    day_of_week  = db.Column(db.String(20))   # Monday | Tuesday | Rest | etc.
    exercises    = db.Column(db.Text)          # JSON: [{exercise_id, sets, reps, rest_sec}]
    is_template  = db.Column(db.Boolean, default=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)


class UserWorkout(db.Model):
    """Completed workout sessions"""
    __tablename__ = 'user_workouts'

    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workout_plan_id = db.Column(db.Integer, db.ForeignKey('workout_plans.id'))
    date            = db.Column(db.Date, default=date.today)
    duration_mins   = db.Column(db.Integer)
    calories_burned = db.Column(db.Float)
    notes           = db.Column(db.Text)
    completed       = db.Column(db.Boolean, default=True)


# ─────────────────────────────────────────────
#  ATTENDANCE
# ─────────────────────────────────────────────
class Attendance(db.Model):
    __tablename__ = 'attendance'

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    check_in    = db.Column(db.DateTime, default=datetime.utcnow)
    check_out   = db.Column(db.DateTime)
    method      = db.Column(db.String(20), default='qr')   # qr | manual

    @property
    def duration_mins(self):
        if self.check_out:
            delta = self.check_out - self.check_in
            return int(delta.total_seconds() / 60)
        return None


# ─────────────────────────────────────────────
#  DIET & FOOD
# ─────────────────────────────────────────────
class FoodEntry(db.Model):
    __tablename__ = 'food_entries'

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date         = db.Column(db.Date, default=date.today)
    meal_type    = db.Column(db.String(20))   # breakfast | lunch | dinner | snack
    food_name    = db.Column(db.String(150))
    quantity_g   = db.Column(db.Float)
    calories     = db.Column(db.Float)
    protein_g    = db.Column(db.Float)
    carbs_g      = db.Column(db.Float)
    fat_g        = db.Column(db.Float)
    cost_inr     = db.Column(db.Float)
    logged_at    = db.Column(db.DateTime, default=datetime.utcnow)


class DietPlan(db.Model):
    __tablename__ = 'diet_plans'

    id           = db.Column(db.Integer, primary_key=True)
    goal         = db.Column(db.String(50))
    calorie_range= db.Column(db.String(30))   # e.g. "1800-2000"
    meals        = db.Column(db.Text)          # JSON: meal plan data
    is_veg       = db.Column(db.Boolean, default=True)
    budget_inr   = db.Column(db.Float)


# ─────────────────────────────────────────────
#  STREAK
# ─────────────────────────────────────────────
class Streak(db.Model):
    __tablename__ = 'streaks'

    id                  = db.Column(db.Integer, primary_key=True)
    user_id             = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    workout_streak      = db.Column(db.Integer, default=0)
    attendance_streak   = db.Column(db.Integer, default=0)
    diet_streak         = db.Column(db.Integer, default=0)
    max_workout_streak  = db.Column(db.Integer, default=0)
    max_attendance_streak= db.Column(db.Integer, default=0)
    total_points        = db.Column(db.Integer, default=0)
    last_workout_date   = db.Column(db.Date)
    last_attendance_date= db.Column(db.Date)
    last_diet_date      = db.Column(db.Date)
    updated_at          = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ─────────────────────────────────────────────
#  WEIGHT LOG (Progress)
# ─────────────────────────────────────────────
class WeightLog(db.Model):
    __tablename__ = 'weight_logs'

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    weight_kg   = db.Column(db.Float, nullable=False)
    body_fat    = db.Column(db.Float)
    muscle_mass = db.Column(db.Float)
    logged_date = db.Column(db.Date, default=date.today)
    notes       = db.Column(db.String(200))


# ─────────────────────────────────────────────
#  NOTIFICATION
# ─────────────────────────────────────────────
class Notification(db.Model):
    __tablename__ = 'notifications'

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title       = db.Column(db.String(150))
    message     = db.Column(db.Text)
    ntype       = db.Column(db.String(30))   # workout | water | payment | streak | system
    is_read     = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
