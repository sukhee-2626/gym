"""Entry point — works for local dev and Railway/Render production"""
import os
from app import create_app, db
from datetime import datetime

app = create_app()

# Make `now()` available in all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now}

# Auto-create tables on first run
with app.app_context():
    db.create_all()
    # If the database is empty, automatically seed it with basic data
    from app.models import User
    if User.query.first() is None:
        try:
            import setup_db
            print("[INFO] Database was empty. Auto-seeded with demo data.")
        except Exception as e:
            print("[ERROR] Failed to auto-seed:", e)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)
