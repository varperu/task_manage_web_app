
from flask import Flask,jsonify,request,session,redirect,url_for
from flask_cors import CORS 

app = Flask(__name__)
CORS(app) 
app.secret_key = "your_secret_key"

users = [
    {'username': 'rutuja', 'password': 'rutuja'},
    {'username': 'admin', 'password': 'admin'},
]

tasks = []

def is_logged_in():
    return 'username' in session

@app.route('/')
def index():
    if is_logged_in():
        return jsonify({'message': 'Welcome to the Task Management App'})
    else:
        return redirect(url_for('login'))
    
@app.route('/login', methods=['POST'])
def login():
    data = request.json or request.form  # Handle both JSON and form data
    username = data.get('username')
    password = data.get('password')

    user = next((user for user in users if user['username'] == username and user['password'] == password), None)
    if user:
        session['username'] = username
        return redirect(url_for('index'))
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if not is_logged_in():
        return jsonify({'error': 'Authentication required'}), 401

    if request.method == 'GET':
        return jsonify({'tasks': tasks})
    elif request.method == 'POST':
        data = request.get_json()
        new_task = {'id': len(tasks) + 1, 'title': data['title']}
        tasks.append(new_task)
        return jsonify({'task': new_task}), 201

@app.route('/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_task(task_id):
    if not is_logged_in():
        return jsonify({'error': 'Authentication required'}), 401

    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    if request.method == 'GET':
        return jsonify({'task': task})
    elif request.method == 'PUT':
        data = request.get_json()
        task['title'] = data['title']
        return jsonify({'task': task}), 200
    elif request.method == 'DELETE':
        tasks = [t for t in tasks if t['id'] != task_id]
        return jsonify({'message': 'Task deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)