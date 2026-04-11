"""Attendance Routes - QR check-in, history"""
import qrcode
import io
import base64
import uuid
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app import db
from app.models import Attendance, User, Streak
from datetime import date, datetime

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/')
@login_required
def index():
    # Generate QR code for user
    qr_data = f"smartgym://checkin/{current_user.qr_token}"
    qr = qrcode.QRCode(version=1, box_size=8, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#7c3aed", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    qr_b64 = base64.b64encode(buf.getvalue()).decode()

    history = Attendance.query.filter_by(
        user_id=current_user.id
    ).order_by(Attendance.check_in.desc()).limit(30).all()

    # Check if already checked in today
    today_attendance = Attendance.query.filter(
        Attendance.user_id == current_user.id,
        db.func.date(Attendance.check_in) == date.today()
    ).first()

    return render_template('attendance/index.html',
        qr_b64=qr_b64,
        history=history,
        today_attendance=today_attendance,
    )


@attendance_bp.route('/checkin', methods=['POST'])
@login_required
def checkin():
    """Manual check-in"""
    today_checkin = Attendance.query.filter(
        Attendance.user_id == current_user.id,
        db.func.date(Attendance.check_in) == date.today()
    ).first()

    if today_checkin:
        return jsonify({"success": False, "message": "Already checked in today!"})

    att = Attendance(user_id=current_user.id, method='manual')
    db.session.add(att)

    # Update attendance streak
    streak = current_user.streaks
    if streak:
        last = streak.last_attendance_date
        yesterday = date.today() - __import__('datetime').timedelta(days=1)
        if last == yesterday:
            streak.attendance_streak += 1
        elif last != date.today():
            streak.attendance_streak = 1
        streak.last_attendance_date = date.today()
        streak.max_attendance_streak = max(streak.attendance_streak, streak.max_attendance_streak)
        streak.total_points += 5

    db.session.commit()
    return jsonify({"success": True, "message": "✅ Checked in successfully!", "streak": streak.attendance_streak if streak else 1})


@attendance_bp.route('/scan/<token>')
def scan_qr(token):
    """QR code scan endpoint"""
    user = User.query.filter_by(qr_token=token).first()
    if not user:
        return jsonify({"error": "Invalid QR code"}), 404

    today_checkin = Attendance.query.filter(
        Attendance.user_id == user.id,
        db.func.date(Attendance.check_in) == date.today()
    ).first()

    if today_checkin:
        return jsonify({"success": False, "message": f"{user.name} already checked in today!"})

    att = Attendance(user_id=user.id, method='qr')
    db.session.add(att)
    db.session.commit()
    return jsonify({"success": True, "message": f"✅ {user.name} checked in via QR!"})


@attendance_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    att = Attendance.query.filter(
        Attendance.user_id == current_user.id,
        db.func.date(Attendance.check_in) == date.today(),
        Attendance.check_out == None
    ).first()
    if att:
        att.check_out = datetime.utcnow()
        db.session.commit()
        return jsonify({"success": True, "duration": att.duration_mins})
    return jsonify({"success": False, "message": "No active check-in found"})


@attendance_bp.route('/api/stats')
@login_required
def api_stats():
    total = Attendance.query.filter_by(user_id=current_user.id).count()
    this_month = Attendance.query.filter(
        Attendance.user_id == current_user.id,
        db.func.strftime('%Y-%m', Attendance.check_in) == date.today().strftime('%Y-%m')
    ).count()
    return jsonify({"total": total, "this_month": this_month})
