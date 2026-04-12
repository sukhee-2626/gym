"""Membership Routes - Plans, enrollment, payment history"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Membership, MembershipPlan, Notification
from datetime import date, timedelta

membership_bp = Blueprint('membership', __name__)


@membership_bp.route('/')
@login_required
def index():
    plans = MembershipPlan.query.filter_by(is_active=True).all()
    active = Membership.query.filter_by(
        user_id=current_user.id, status='active'
    ).order_by(Membership.end_date.desc()).first()
    history = Membership.query.filter_by(
        user_id=current_user.id
    ).order_by(Membership.created_at.desc()).all()
    return render_template('membership/index.html',
        plans=plans,
        active=active,
        history=history,
    )


@membership_bp.route('/enroll/<int:plan_id>', methods=['POST'])
@login_required
def enroll(plan_id):
    plan = MembershipPlan.query.get_or_404(plan_id)

    # Expire existing active membership
    existing = Membership.query.filter_by(
        user_id=current_user.id, status='active'
    ).first()
    if existing:
        existing.status = 'expired'

    start = date.today()
    end = start + timedelta(days=plan.duration_days)
    m = Membership(
        user_id=current_user.id,
        plan_id=plan.id,
        start_date=start,
        end_date=end,
        amount_paid=plan.price,
        payment_mode=request.form.get('payment_mode', 'cash'),
        status='active',
    )
    db.session.add(m)

    # Notification
    notif = Notification(
        user_id=current_user.id,
        title="Membership Activated 🎉",
        message=f"Your {plan.name} plan is active till {end.strftime('%d %b %Y')}.",
        ntype='payment',
    )
    db.session.add(notif)
    db.session.commit()

    flash(f'✅ Successfully enrolled in the {plan.name} plan!', 'success')
    return redirect(url_for('membership.index'))


@membership_bp.route('/api/plans')
def api_plans():
    plans = MembershipPlan.query.filter_by(is_active=True).all()
    return jsonify([{
        "id": p.id, "name": p.name, "price": p.price,
        "duration_days": p.duration_days, "features": p.features,
    } for p in plans])
