"""Admin Panel Routes - Members, Fees, Attendance, Exercises"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Membership, MembershipPlan, Attendance, Exercise, Streak
from datetime import date, timedelta
from functools import wraps

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Admin access required.', 'error')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/')
@admin_required
def index():
    """Admin dashboard with key stats"""
    total_members = User.query.filter_by(role='member').count()
    active_memberships = Membership.query.filter_by(status='active').count()
    today_attendance = Attendance.query.filter(
        db.func.date(Attendance.check_in) == date.today()
    ).count()
    total_revenue = db.session.query(db.func.sum(Membership.amount_paid)).scalar() or 0

    # Recent members
    recent_members = User.query.filter_by(role='member').order_by(User.created_at.desc()).limit(10).all()
    # Expiring soon (within 7 days)
    expiring = Membership.query.filter(
        Membership.status == 'active',
        Membership.end_date <= date.today() + timedelta(days=7)
    ).all()

    return render_template('admin/index.html',
        total_members=total_members,
        active_memberships=active_memberships,
        today_attendance=today_attendance,
        total_revenue=total_revenue,
        recent_members=recent_members,
        expiring=expiring,
    )


@admin_bp.route('/members')
@admin_required
def members():
    """All members list with membership & attendance info"""
    search = request.args.get('q', '')
    query = User.query.filter_by(role='member')
    if search:
        query = query.filter(
            db.or_(User.name.ilike(f'%{search}%'), User.email.ilike(f'%{search}%'))
        )
    members = query.order_by(User.created_at.desc()).all()

    # Attach active membership to each member
    for m in members:
        m.active_membership = Membership.query.filter_by(
            user_id=m.id, status='active'
        ).order_by(Membership.end_date.desc()).first()

    return render_template('admin/members.html', members=members, search=search)


@admin_bp.route('/members/<int:user_id>')
@admin_required
def member_detail(user_id):
    """Single member detail: memberships, attendance"""
    member = User.query.get_or_404(user_id)
    memberships = Membership.query.filter_by(user_id=user_id).order_by(Membership.created_at.desc()).all()
    attendance = Attendance.query.filter_by(user_id=user_id).order_by(Attendance.check_in.desc()).limit(30).all()
    streak = member.streaks
    return render_template('admin/member_detail.html',
        member=member, memberships=memberships, attendance=attendance, streak=streak)


@admin_bp.route('/fees')
@admin_required
def fees():
    """All membership fees / payments"""
    memberships = Membership.query.join(User).join(MembershipPlan)\
        .order_by(Membership.created_at.desc()).all()
    total_revenue = db.session.query(db.func.sum(Membership.amount_paid)).scalar() or 0
    active_count = Membership.query.filter_by(status='active').count()
    expired_count = Membership.query.filter_by(status='expired').count()
    return render_template('admin/fees.html',
        memberships=memberships,
        total_revenue=total_revenue,
        active_count=active_count,
        expired_count=expired_count,
    )


@admin_bp.route('/attendance')
@admin_required
def attendance():
    """All attendance records"""
    filter_date = request.args.get('date', date.today().isoformat())
    try:
        filter_date_obj = date.fromisoformat(filter_date)
    except ValueError:
        filter_date_obj = date.today()

    records = Attendance.query.join(User).filter(
        db.func.date(Attendance.check_in) == filter_date_obj
    ).order_by(Attendance.check_in.desc()).all()

    today_count = Attendance.query.filter(
        db.func.date(Attendance.check_in) == date.today()
    ).count()

    return render_template('admin/attendance.html',
        records=records,
        filter_date=filter_date,
        today_count=today_count,
    )


@admin_bp.route('/exercises')
@admin_required
def exercises():
    """List all exercises - admin can add/edit/delete"""
    goal_filter = request.args.get('goal', '')
    query = Exercise.query
    if goal_filter:
        query = query.filter(Exercise.goal_tag.ilike(f'%{goal_filter}%'))
    exercises = query.order_by(Exercise.goal_tag, Exercise.name).all()
    return render_template('admin/exercises.html', exercises=exercises, goal_filter=goal_filter)


@admin_bp.route('/exercises/add', methods=['GET', 'POST'])
@admin_required
def add_exercise():
    if request.method == 'POST':
        data = request.form
        ex = Exercise(
            name=data['name'],
            muscle_group=data.get('muscle_group', ''),
            equipment=data.get('equipment', 'bodyweight'),
            difficulty=data.get('difficulty', 'beginner'),
            calories_per_min=float(data.get('calories_per_min', 5)),
            description=data.get('description', ''),
            youtube_url=data.get('youtube_url', ''),
            goal_tag=data.get('goal_tag', 'all'),
            sets_recommended=int(data.get('sets_recommended', 3)),
            reps_recommended=data.get('reps_recommended', '12'),
            rest_seconds=int(data.get('rest_seconds', 60)),
        )
        db.session.add(ex)
        db.session.commit()
        flash(f'Exercise "{ex.name}" added successfully!', 'success')
        return redirect(url_for('admin.exercises'))
    return render_template('admin/exercise_form.html', exercise=None)


@admin_bp.route('/exercises/<int:ex_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_exercise(ex_id):
    ex = Exercise.query.get_or_404(ex_id)
    if request.method == 'POST':
        data = request.form
        ex.name = data['name']
        ex.muscle_group = data.get('muscle_group', ex.muscle_group)
        ex.equipment = data.get('equipment', ex.equipment)
        ex.difficulty = data.get('difficulty', ex.difficulty)
        ex.calories_per_min = float(data.get('calories_per_min', ex.calories_per_min))
        ex.description = data.get('description', ex.description)
        ex.youtube_url = data.get('youtube_url', ex.youtube_url)
        ex.goal_tag = data.get('goal_tag', ex.goal_tag)
        ex.sets_recommended = int(data.get('sets_recommended', ex.sets_recommended))
        ex.reps_recommended = data.get('reps_recommended', ex.reps_recommended)
        ex.rest_seconds = int(data.get('rest_seconds', ex.rest_seconds))
        db.session.commit()
        flash(f'Exercise "{ex.name}" updated!', 'success')
        return redirect(url_for('admin.exercises'))
    return render_template('admin/exercise_form.html', exercise=ex)


@admin_bp.route('/exercises/<int:ex_id>/delete', methods=['POST'])
@admin_required
def delete_exercise(ex_id):
    ex = Exercise.query.get_or_404(ex_id)
    db.session.delete(ex)
    db.session.commit()
    flash(f'Exercise "{ex.name}" deleted.', 'success')
    return redirect(url_for('admin.exercises'))


@admin_bp.route('/members/<int:user_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_member_status(user_id):
    member = User.query.get_or_404(user_id)
    member.is_active = not member.is_active
    db.session.commit()
    status = 'activated' if member.is_active else 'deactivated'
    flash(f'{member.name} has been {status}.', 'success')
    return redirect(url_for('admin.member_detail', user_id=user_id))


@admin_bp.route('/api/stats')
@admin_required
def api_stats():
    """JSON stats for admin dashboard charts"""
    # Attendance last 7 days
    attendance_data = []
    for i in range(6, -1, -1):
        d = date.today() - timedelta(days=i)
        count = Attendance.query.filter(db.func.date(Attendance.check_in) == d).count()
        attendance_data.append({'date': d.strftime('%a'), 'count': count})

    # Revenue by plan
    revenue_by_plan = db.session.query(
        MembershipPlan.name,
        db.func.sum(Membership.amount_paid).label('total')
    ).join(Membership).group_by(MembershipPlan.name).all()

    return jsonify({
        'attendance': attendance_data,
        'revenue_by_plan': [{'plan': r.name, 'total': r.total or 0} for r in revenue_by_plan],
    })
