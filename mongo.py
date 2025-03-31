import pymongo
import bcrypt

# MongoDB Connection
MONGO_URI = "mongodb+srv://hardikjain:hardik@cluster0.smd4cqi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client["todolist"]
    users_collection = db["users"]
    tasks_collection = db["tasks"]

    print("Connected to MongoDB Atlas Successfully!")

    # Function to register a new user
    def register():
        name = input("Enter your name: ")
        password = input("Enter a password: ")

        # Check if user already exists
        existing_user = users_collection.find_one({"name": name})
        if existing_user:
            print("User already exists! Try logging in.")
            return None

        # Hash the password
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert user into DB
        users_collection.insert_one({"name": name, "password": hashed_pw})
        print("User registered successfully! Please log in.")

    # Function to authenticate user login
    def login():
        name = input("Enter your name: ")
        password = input("Enter your password: ")

        # Fetch user from DB
        user = users_collection.find_one({"name": name})
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            print("Login successful!")
            return name  # Return username for further actions
        else:
            print("Invalid credentials!")
            return None

    # Function to add a new task
    def add_task(user):
        task = input("Enter your task: ")
        tasks_collection.insert_one({"user": user, "task": task, "completed": False})
        print("Task added successfully!")

    # Function to delete a task
    def delete_task(user):
        task = input("Enter the task to delete: ")
        result = tasks_collection.delete_one({"user": user, "task": task})
        if result.deleted_count > 0:
            print("Task deleted successfully!")
        else:
            print("Task not found!")

    # Function to mark a task as completed
    def complete_task(user):
        task = input("Enter the task to mark as completed: ")
        result = tasks_collection.update_one(
            {"user": user, "task": task}, 
            {"$set": {"completed": True}}
        )
        if result.modified_count > 0:
            print("Task marked as completed!")
        else:
            print("Task not found!")

    # Function to view tasks
    def view_tasks(user):
        tasks = tasks_collection.find({"user": user})
        print("\nYour To-Do List:")
        for task in tasks:
            status = "✅" if task["completed"] else "❌"
            print(f"{status} {task['task']}")
        print("")

    # Main Menu
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                while True:
                    print("\n1. Add Task")
                    print("2. Delete Task")
                    print("3. Mark Task as Completed")
                    print("4. View Tasks")
                    print("5. Logout")
                    action = input("Enter your choice: ")

                    if action == "1":
                        add_task(user)
                    elif action == "2":
                        delete_task(user)
                    elif action == "3":
                        complete_task(user)
                    elif action == "4":
                        view_tasks(user)
                    elif action == "5":
                        print("Logged out successfully!")
                        break
                    else:
                        print("Invalid choice! Try again.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Try again.")

except Exception as e:
    print("Error:", e)
