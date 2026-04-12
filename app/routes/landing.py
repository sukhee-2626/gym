"""Landing Page Route"""
from flask import Blueprint, render_template
from app.models import MembershipPlan

landing_bp = Blueprint('landing', __name__)


@landing_bp.route('/')
def index():
    plans = MembershipPlan.query.filter_by(is_active=True).all()
    return render_template('landing/index.html', plans=plans)

@landing_bp.route('/sw.js')
def sw():
    from flask import send_from_directory, current_app
    return send_from_directory(current_app.static_folder, 'sw.js', mimetype='application/javascript')

@landing_bp.route('/manifest.json')
def manifest():
    from flask import send_from_directory, current_app
    return send_from_directory(current_app.static_folder, 'manifest.json', mimetype='application/json')
