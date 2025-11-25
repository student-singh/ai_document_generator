# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from database import db   # ← FIXED: import from database.py

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if db.users.find_one({"email": email}):
            flash("Email already registered!")
            return redirect(url_for('auth.register'))
            
        hashed = generate_password_hash(password)
        user_id = db.users.insert_one({
            "email": email,
            "password": hashed
        }).inserted_id
        
        user = User(user_id, email)
        login_user(user)
        return redirect(url_for('project.dashboard'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = db.users.find_one({"email": email})
        
        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data['_id'], email)
            login_user(user)
            return redirect(url_for('project.dashboard'))
        
        flash("Invalid email or password")
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))