import os
import sys
import logging

from flask import Flask, request, jsonify
from flask_cors import CORS

from models import db, User, Task
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

@app.before_request
def before_request():
    db.connect()

@app.teardown_request
def teardown_request(exception):
    db.close()

@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.select()
    return jsonify([user.to_dict() for user in users])

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.select().where(Task.user == request.args.get("user_id"))
    return jsonify([task.to_dict() for task in tasks])

@app.route("/api/tasks", methods=["POST"])
def create_task():
    task = Task.create(**request.json)
    return jsonify(task.to_dict())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.run(host='0.0.0.0', port=port)
    else:
        app.run(host='0.0.0.0', port=port, debug=True)