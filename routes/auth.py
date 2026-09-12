from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config import db
from models import User, user_schema
from marshmallow import ValidationError

class SignUp(Resource):
    def post(self):
        try:
            data = user_schema.load(request.get_json())
        except ValidationError as err:
            return {"errors": err.messages}, 400

        if User.query.filter_by(username=data['username']).first():
            return {"error": "Username already exists"}, 400

        new_user = User(username=data['username'])
        new_user.password_hash = data['password']

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id)
        return {"user": user_schema.dump(new_user), "token": access_token}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(password):
            access_token = create_access_token(identity=user.id)
            return {"user": user_schema.dump(user), "token": access_token}, 200
        
        return {"error": "Invalid username or password"}, 401

class CheckSession(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user_schema.dump(user), 200
