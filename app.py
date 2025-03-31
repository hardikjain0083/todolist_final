from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)

# MongoDB Connection
client = pymongo.MongoClient("mongodb+srv://hardikjain:hardik@cluster0.smd4cqi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["todolist"]
users_collection = db["users"]
tasks_collection = db["tasks"]

# User Registration
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data["name"]
    password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    if users_collection.find_one({"name": name}):
        return jsonify({"message": "User already exists"}), 400

    users_collection.insert_one({"name": name, "password": password})
    return jsonify({"message": "User registered successfully!"})

# User Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = users_collection.find_one({"name": data["name"]})

    if user and bcrypt.check_password_hash(user["password"], data["password"]):
        session["user"] = data["name"]
        return jsonify({"message": "Login successful!"})
    return jsonify({"message": "Invalid credentials"}), 401

# Add Task
@app.route("/add_task", methods=["POST"])
def add_task():
    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json
    task = {
        "user": session["user"],
        "task": data["task"],
        "completed": False
    }
    tasks_collection.insert_one(task)
    return jsonify({"message": "Task added successfully!"})

# Get Tasks
@app.route("/get_tasks", methods=["GET"])
def get_tasks():
    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    tasks = list(tasks_collection.find({"user": session["user"]}))
    # Convert ObjectId to string for JSON serialization
    for task in tasks:
        task["_id"] = str(task["_id"])
    return jsonify(tasks)

# Update Task Completion Status
@app.route("/complete_task", methods=["POST"])
def complete_task():
    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json
    tasks_collection.update_one(
        {"_id": ObjectId(data["taskId"]), "user": session["user"]},
        {"$set": {"completed": data["completed"]}}
    )
    return jsonify({"message": "Task status updated!"})

# Update Task Text
@app.route("/update_task", methods=["POST"])
def update_task():
    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json
    tasks_collection.update_one(
        {"_id": ObjectId(data["taskId"]), "user": session["user"]},
        {"$set": {"task": data["newTask"]}}
    )
    return jsonify({"message": "Task updated successfully!"})

# Delete Task
@app.route("/delete_task", methods=["POST"])
def delete_task():
    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json
    tasks_collection.delete_one({
        "_id": ObjectId(data["taskId"]),
        "user": session["user"]
    })
    return jsonify({"message": "Task deleted successfully!"})

# Logout
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"message": "Logged out successfully"})

if __name__ == "__main__":
    app.run(debug=True)