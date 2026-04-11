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


@membership_bp.route('/enroll', methods=['POST'])
@login_required
def enroll():
    data = request.get_json()
    plan = MembershipPlan.query.get(data.get('plan_id'))
    if not plan:
        return jsonify({"success": False, "message": "Plan not found"})

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
        payment_mode=data.get('payment_mode', 'cash'),
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

    return jsonify({"success": True, "ends": end.strftime('%d %b %Y'), "plan": plan.name})


@membership_bp.route('/api/plans')
def api_plans():
    plans = MembershipPlan.query.filter_by(is_active=True).all()
    return jsonify([{
        "id": p.id, "name": p.name, "price": p.price,
        "duration_days": p.duration_days, "features": p.features,
    } for p in plans])
