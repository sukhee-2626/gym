"""Entry point — works for local dev and Railway/Render production"""
import os
from app import create_app, db
from datetime import datetime

app = create_app()

# Make `now()` available in all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now}

# Auto-create tables on first run (useful for cloud deployment)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)
