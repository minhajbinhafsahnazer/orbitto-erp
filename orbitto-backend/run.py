#!/usr/bin/env python
import os
from dotenv import load_dotenv
from app import create_app, db

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Create shell context for flask shell"""
    return {'db': db}

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('Database initialized!')

@app.cli.command()
def drop_db():
    """Drop all database tables"""
    db.drop_all()
    print('Database dropped!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
