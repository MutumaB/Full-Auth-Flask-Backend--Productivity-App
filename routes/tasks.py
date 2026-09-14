from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import db
from models import Task, task_schema, tasks_schema
from marshmallow import ValidationError

class TaskListResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Access protection constraints isolating resource queries strictly to the token owner
        pagination = Task.query.filter_by(user_id=current_user_id).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return {
            "tasks": tasks_schema.dump(pagination.items),
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total_items": pagination.total,
            "total_pages": pagination.pages
        }, 200

    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        try:
            data = task_schema.load(request.get_json())
        except ValidationError as err:
            return {"errors": err.messages}, 400

        new_task = Task(
            title=data['title'],
            description=data.get('description'),
            is_completed=data.get('is_completed', False),
            user_id=current_user_id
        )
        db.session.add(new_task)
        db.session.commit()
        return task_schema.dump(new_task), 201


class TaskResource(Resource):
    @jwt_required()
    def get(self, id):
        current_user_id = get_jwt_identity()
        task = Task.query.filter_by(id=id, user_id=current_user_id).first()
        
        if not task:
            return {"error": "Resource not found or unauthorized access"}, 404
            
        return task_schema.dump(task), 200

    @jwt_required()
    def patch(self, id):
        current_user_id = get_jwt_identity()
        task = Task.query.filter_by(id=id, user_id=current_user_id).first()
        
        if not task:
            return {"error": "Resource not found or unauthorized access"}, 404

        try:
            data = task_schema.load(request.get_json(), partial=True)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'is_completed' in data:
            task.is_completed = data['is_completed']

        db.session.commit()
        return task_schema.dump(task), 200

    @jwt_required()
    def delete(self, id):
        current_user_id = get_jwt_identity()
        task = Task.query.filter_by(id=id, user_id=current_user_id).first()
        
        if not task:
            return {"error": "Resource not found or unauthorized access"}, 404

        db.session.delete(task)
        db.session.commit()
        return {"message": "Resource deleted successfully"}, 200
