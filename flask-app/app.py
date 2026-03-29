from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import redis
import os

app = Flask(__name__)

# Configuration PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# Configuration Redis
cache = redis.Redis(host='redis', port=6379)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Utilisation de Redis pour compter les visites (Partie 3)
    visits = cache.incr('hits')
    tasks = Task.query.all()
    return jsonify({
        "tasks": [{"id": t.id, "title": t.title} for t in tasks],
        "visit_count": visits
    })

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task created"}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)