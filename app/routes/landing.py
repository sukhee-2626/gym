"""Landing Page Route"""
from flask import Blueprint, render_template
from app.models import MembershipPlan

landing_bp = Blueprint('landing', __name__)


@landing_bp.route('/')
def index():
    plans = MembershipPlan.query.filter_by(is_active=True).all()
    return render_template('landing/index.html', plans=plans)
