const apiUrl = "http://127.0.0.1:5000";
let currentEditTaskId = null;

// DOM Elements
const authSection = document.getElementById("auth-section");
const taskSection = document.getElementById("task-section");
const taskInput = document.getElementById("task-input");
const taskList = document.getElementById("task-list");
const editModal = document.getElementById("edit-modal");
const editTaskInput = document.getElementById("edit-task-input");

// Auth Functions
async function register() {
    const name = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch(apiUrl + "/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, password })
    });

    const data = await response.json();
    alert(data.message);
}

async function login() {
    const name = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch(apiUrl + "/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, password }),
        credentials: 'include' // Important for session cookies
    });

    const data = await response.json();
    if (response.ok) {
        authSection.style.display = "none";
        taskSection.style.display = "block";
        document.getElementById("user-name").innerText = name;
        getTasks();
    } else {
        alert(data.message);
    }
}

// Task Functions
async function addTask() {
    const task = taskInput.value.trim();
    if (!task) return;

    await fetch(apiUrl + "/add_task", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task }),
        credentials: 'include'
    });

    taskInput.value = "";
    getTasks();
}

async function getTasks() {
    const response = await fetch(apiUrl + "/get_tasks", {
        credentials: 'include'
    });
    const tasks = await response.json();
    
    taskList.innerHTML = tasks.map(task => `
        <li class="task-item" data-id="${task._id}">
            <span class="task-text ${task.completed ? 'completed' : ''}">${task.task}</span>
            <div class="task-actions">
                <button onclick="toggleComplete('${task._id}', ${task.completed})">
                    ${task.completed ? '❌ Undo' : '✅ Complete'}
                </button>
                <button onclick="openEditModal('${task._id}', '${task.task}')">✏️ Edit</button>
                <button onclick="deleteTask('${task._id}')">🗑️ Delete</button>
            </div>
        </li>
    `).join("");
}

async function toggleComplete(taskId, isCompleted) {
    await fetch(apiUrl + "/complete_task", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            taskId,
            completed: !isCompleted 
        }),
        credentials: 'include'
    });
    getTasks();
}

function openEditModal(taskId, currentText) {
    currentEditTaskId = taskId;
    editTaskInput.value = currentText;
    editModal.style.display = "block";
}

function closeEditModal() {
    editModal.style.display = "none";
}

async function updateTask() {
    const newText = editTaskInput.value.trim();
    if (!newText) return;

    await fetch(apiUrl + "/update_task", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            taskId: currentEditTaskId,
            newTask: newText 
        }),
        credentials: 'include'
    });

    closeEditModal();
    getTasks();
}

async function deleteTask(taskId) {
    if (!confirm("Are you sure you want to delete this task?")) return;
    
    await fetch(apiUrl + "/delete_task", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ taskId }),
        credentials: 'include'
    });
    getTasks();
}

function logout() {
    fetch(apiUrl + "/logout", {
        credentials: 'include'
    }).then(() => {
        location.reload();
    });
}

// Close modal when clicking outside of it
window.onclick = function(event) {
    if (event.target == editModal) {
        closeEditModal();
    }
}