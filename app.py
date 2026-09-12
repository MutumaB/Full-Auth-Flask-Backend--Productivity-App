from config import app, api
from routes.auth import SignUp, Login, CheckSession
from routes.tasks import TaskListResource, TaskResource

# Map Endpoints to Resources
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(CheckSession, '/check_session')

api.add_resource(TaskListResource, '/tasks')
api.add_resource(TaskResource, '/tasks/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
