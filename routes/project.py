# routes/project.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from bson import ObjectId
from models.project import Project
from utils.gemini import generate, suggest_outline
from database import db

project_bp = Blueprint('project', __name__, url_prefix='/project')

@project_bp.route('/dashboard')
@login_required
def dashboard():
    projects = list(db.projects.find({"user_id": current_user.id}))
    for p in projects:
        p['_id'] = str(p['_id'])
    return render_template('dashboard.html', projects=projects)

@project_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        structure = request.form.getlist('structure[]')
        project = Project(
            user_id=current_user.id,
            title=request.form['title'],
            doc_type=request.form['doc_type'],
            topic=request.form['topic'],
            structure=structure
        )
        result = db.projects.insert_one(project.to_dict())
        return redirect(url_for('project.editor', project_id=str(result.inserted_id)))
    return render_template('project_new.html')

@project_bp.route('/suggest-outline', methods=['POST'])
def suggest_outline_route():
    data = request.json
    suggestions = suggest_outline(data['topic'], data['doc_type'])
    return jsonify({"suggestions": suggestions})

@project_bp.route('/<project_id>/editor')
@login_required
def editor(project_id):
    project = db.projects.find_one({
        "_id": ObjectId(project_id),
        "user_id": current_user.id
    })
    if not project:
        return "Not found", 404
    project['_id'] = str(project['_id'])
    return render_template('editor.html', project=project)

@project_bp.route('/<project_id>/update-outline', methods=['PATCH'])
@login_required
def update_outline(project_id):
    data = request.json
    db.projects.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": {"structure": data['structure']}}
    )
    return jsonify({"status": "saved"})

@project_bp.route('/<project_id>/generate', methods=['POST'])
@login_required
def generate_content(project_id):
    project = db.projects.find_one({"_id": ObjectId(project_id)})
    titles = project['structure']
    prev = ""
    for i, title in enumerate(titles):
        prompt = f"Topic: {project['topic']}\nPrevious: {prev[-800:]}\nWrite section: {title}"
        text = generate(prompt)
        db.projects.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": {f"content.{i}": {"text": text, "prompt_used": prompt}}}
        )
        prev = text
    return jsonify({"status": "done"})