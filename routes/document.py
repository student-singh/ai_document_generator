# routes/document.py
from flask import Blueprint, jsonify, send_file, request
from flask_login import login_required, current_user
from bson import ObjectId
from datetime import datetime
from utils.gemini import refine_with_context
from utils.docx_generator import create_docx
from utils.pptx_generator import create_pptx
from database import db  # ← FIXED: No circular import

document_bp = Blueprint('document', __name__, url_prefix='/document')

# Refine one section
@document_bp.route('/<project_id>/refine/<int:idx>', methods=['POST'])
@login_required
def refine_section(project_id, idx):
    data = request.json
    project = db.projects.find_one({"_id": ObjectId(project_id), "user_id": current_user.id})
    if not project:
        return jsonify({"error": "Not found"}), 404

    current_text = data.get('current_text', '')
    user_prompt = data.get('prompt', 'Improve this section').strip()

    # Get previous content for context
    prev_content = ""
    for i in range(idx):
        prev_text = project['content'].get(str(i), {}).get('text', '')
        if prev_text:
            prev_content += prev_text + " "

    new_text = refine_with_context(current_text, user_prompt, prev_content)

    # Save refined text + history
    db.projects.update_one(
        {"_id": ObjectId(project_id)},
        {
            "$set": {f"content.{idx}.text": new_text},
            "$push": {
                "history": {
                    "type": "refine",
                    "section": idx,
                    "prompt": user_prompt,
                    "timestamp": datetime.utcnow()
                }
            }
        }
    )

    return jsonify({"text": new_text})

# Like / Dislike / Comment
@document_bp.route('/<project_id>/feedback/<int:idx>', methods=['POST'])
@login_required
def save_feedback(project_id, idx):
    data = request.json
    action = data['action']  # like, dislike, comment
    comment = data.get('comment', '')

    db.projects.update_one(
        {"_id": ObjectId(project_id), "user_id": current_user.id},
        {"$push": {
            "history": {
                "type": action,
                "section": idx,
                "comment": comment,
                "timestamp": datetime.utcnow()
            }
        }}
    )

    return jsonify({"status": "saved"})

# Export final file
@document_bp.route('/<project_id>/export')
@login_required
def export_document(project_id):
    project = db.projects.find_one({"_id": ObjectId(project_id), "user_id": current_user.id})
    if not project:
        return "Project not found", 404

    try:
        if project['doc_type'] == 'docx':
            filepath = create_docx(project)
            filename = f"{project['title']}.docx"
        else:
            filepath = create_pptx(project)
            filename = f"{project['title']}.pptx"

        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document' if project['doc_type'] == 'docx'
                     else 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
    except Exception as e:
        return f"Export failed: {str(e)}", 500