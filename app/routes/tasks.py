from datetime import date
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Task

tasks_bp = Blueprint("tasks", __name__)
VALID_STATUSES = {"pending", "in_progress", "completed"}
VALID_PRIORITIES = {"low", "medium", "high"}

def current_user_id():
    return int(get_jwt_identity())

def validate_task_data(data, partial=False):
    errors = {}
    if not partial or "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            errors["title"] = "title is required"
        elif len(title) > 160:
            errors["title"] = "title must be 160 characters or fewer"
    if "status" in data and data["status"] not in VALID_STATUSES:
        errors["status"] = "status must be pending, in_progress or completed"
    if "priority" in data and data["priority"] not in VALID_PRIORITIES:
        errors["priority"] = "priority must be low, medium or high"
    if "due_date" in data and data["due_date"]:
        try:
            date.fromisoformat(data["due_date"])
        except (TypeError, ValueError):
            errors["due_date"] = "due_date must use YYYY-MM-DD format"
    return errors

@tasks_bp.get("")
@jwt_required()
def list_tasks():
    query = Task.query.filter_by(user_id=current_user_id())
    status = request.args.get("status")
    if status:
        if status not in VALID_STATUSES:
            return jsonify({"error": "Invalid status filter"}), 400
        query = query.filter_by(status=status)

    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 100)
    if page < 1 or per_page < 1:
        return jsonify({"error": "page and per_page must be positive"}), 400

    pagination = query.order_by(Task.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return jsonify({
        "items": [task.to_dict() for task in pagination.items],
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total_items": pagination.total,
            "total_pages": pagination.pages
        }
    }), 200

@tasks_bp.post("")
@jwt_required()
def create_task():
    data = request.get_json(silent=True) or {}
    errors = validate_task_data(data)
    if errors:
        return jsonify({"errors": errors}), 400

    due_date = date.fromisoformat(data["due_date"]) if data.get("due_date") else None
    task = Task(
        title=data["title"].strip(),
        description=(data.get("description") or "").strip(),
        status=data.get("status", "pending"),
        priority=data.get("priority", "medium"),
        due_date=due_date,
        user_id=current_user_id()
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created", "task": task.to_dict()}), 201

@tasks_bp.get("/<int:task_id>")
@jwt_required()
def get_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user_id()).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"task": task.to_dict()}), 200

@tasks_bp.patch("/<int:task_id>")
@jwt_required()
def update_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user_id()).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json(silent=True) or {}
    errors = validate_task_data(data, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400

    for field in ("title", "description", "status", "priority"):
        if field in data:
            value = data[field]
            setattr(task, field, value.strip() if isinstance(value, str) and field in {"title", "description"} else value)
    if "due_date" in data:
        task.due_date = date.fromisoformat(data["due_date"]) if data["due_date"] else None

    db.session.commit()
    return jsonify({"message": "Task updated", "task": task.to_dict()}), 200

@tasks_bp.delete("/<int:task_id>")
@jwt_required()
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user_id()).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"}), 200
