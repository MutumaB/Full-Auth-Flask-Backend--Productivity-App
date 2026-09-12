from config import db, bcrypt
from marshmallow import Schema, fields, validate

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)

    tasks = db.relationship('Task', backref='user', lazy=True, cascade="all, delete-orphan")

    @property
    def password_hash(self):
        raise AttributeError('Password hash is not readable.')

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# Validation & Serialization Schemas
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=6))

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(allow_none=True)
    is_completed = fields.Bool()
    user_id = fields.Int(dump_only=True)

user_schema = UserSchema()
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
