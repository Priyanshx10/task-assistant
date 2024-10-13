from flask import jsonify, request
from app import db
from app.models import Task
from app.utils import parse_date
from app.nlp_processor import process_nlp_query
from datetime import datetime
from app import create_app

app = create_app()

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        due_date=parse_date(data.get('due_date')),
        completed=data.get('completed', False)
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.due_date = parse_date(data.get('due_date')) or task.due_date
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

@app.route('/api/nlp', methods=['POST'])
def nlp_query():
    query = request.json.get('query')
    result = process_nlp_query(query)
    return jsonify(result)