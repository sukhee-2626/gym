"""Entry point"""
from app import create_app, db
from datetime import datetime

app = create_app()

# Make `now()` available in all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
