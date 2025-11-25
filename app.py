# app.py   ← FINAL CLEAN VERSION
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Import db from database.py (no circular import!)
from database import db

from models.user import User

@login_manager.user_loader
def load_user(user_id):
    user_data = db.users.find_one({"_id": user_id})
    if user_data:
        return User(user_data['_id'], user_data['email'])
    return None

# Register blueprints (safe now)
from routes.auth import auth_bp
from routes.project import project_bp
from routes.document import document_bp

app.register_blueprint(auth_bp)
app.register_blueprint(project_bp)
app.register_blueprint(document_bp)

if __name__ == '__main__':
    app.run(debug=True)