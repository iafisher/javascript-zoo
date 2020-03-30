const ENTER_KEY_CODE = 13;
let state = {
    id: 0,
    name: "",
    tasks: [],
}

window.onload = initializePage();

async function initializePage() {
    await fetchTasks();
    generateTasksList(state.tasks);
}

async function fetchTasks() {
    const response = await fetch('/api/project/get?id=1');
    const data = await response.json();
    const { tasks, id } = data;

    state.tasks = tasks;
    state.id = id;
}

async function api(url, payload) {
    console.log("Posting data to " + url, payload);
    // Django requires a server-generated CSRF token to be included with all POST
    // requests.
    const csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const options = {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrf,
        },
        body: JSON.stringify(payload),
    };
    const response = await fetch(url, options);
    return await response.json();
}


// Create task input area
function generateCreateTaskNode() {
    const createTaskNode = document.createElement('div');
    createTaskNode.className = "new-task-form"

    const createTaskLabel = generateCreateTaskLabel();
    const createTaskInput = getCreateTaskInput();

    createTaskNode.appendChild(createTaskLabel);
    createTaskNode.appendChild(createTaskInput);

    return createTaskNode
}

function handleNewTaskInput(event) {
    if (event.keyCode === ENTER_KEY_CODE) {
        event.preventDefault();
        const description = event.target.value
        createNewTask(description)
        newTaskInput = document.getElementById("new-task-input")
        newTaskInput.value = ""
    }
}


// Task
function generateTask(task) {
    const { shortDescription, longDescription, id, status } = task;
    const taskDiv = document.createElement("DIV");
    taskDiv.className = "status-" + status;
    taskDiv.id = id;

    const taskHeader = document.createElement("H2");
    taskHeader.innerHTML = status == "pending" ? shortDescription : "<s>" + shortDescription + "</s>";
    taskHeader.id = id + "-header";
    taskDiv.appendChild(taskHeader);

    const taskStatusDropdown = generateTaskStatusDropdown(id, status);
    taskDiv.appendChild(taskStatusDropdown);

    return taskDiv
}

function generateTaskStatusDropdown(id, status) {
    const statuses = ["pending", "completed"]
    const taskStatusDropdown = document.createElement("SELECT");
    statuses.forEach(status => {
        const opt = document.createElement("OPTION");
        opt.innerText = status;
        taskStatusDropdown.appendChild(opt);
    })

    taskStatusDropdown.addEventListener('change', () => handleStatusChange(event, id))
    taskStatusDropdown.value = status;

    return taskStatusDropdown;
}

async function handleStatusChange(event, id) {
    const newStatus = event.target.value;
    const payload = {
        id: id,
        status: newStatus,
    };
    const responseJson = await api("/api/task/update/status", payload);
    if (responseJson.error) {
        console.error(responseJson.error)
        // TODO: Display a message to the user.
        return;
    }
    status = newStatus;
    const task = document.getElementById(id);
    task.className = "status-" + status;
    const taskHeader = document.getElementById(id + "-header");

    taskHeader.innerHTML = status == "pending" ? taskHeader.innerText : "<s>" + taskHeader.innerText + "</s>";
}


// Tasks list
function generateTasksList(tasks) {
    const tasksListDiv = document.getElementById("tasks-list")
    tasks.map(task => {
        const generatedTask = generateTask(task);
        tasksListDiv.appendChild(generatedTask);
    })
    return tasksListDiv
}

async function createNewTask(description) {
    const payload = {
        description: description,
        order: state.tasks.length,
        parentId: null,
        projectId: state.id,
    };
    const newTask = await api("/api/task/create", payload);
    const tasksList = document.getElementById("tasks-list");
    state.tasks.push(newTask);
    tasksList.appendChild(generateTask(newTask))
}