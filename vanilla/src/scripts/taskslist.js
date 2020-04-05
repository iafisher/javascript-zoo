function generateTask(task) {
    const { shortDescription, longDescription, id, status } = task;
    const statuses = ["pending", "completed"]
    const taskDiv = document.createElement("DIV");
    taskDiv.className = "status-" + status;
    taskDiv.id = id;

    const taskHeader = document.createElement("H2");
    taskHeader.innerText = shortDescription;

    const taskStatus = document.createElement("SELECT");
    statuses.map(status => {
        const opt = document.createElement("OPTION");
        opt.innerText = status;
        taskStatus.appendChild(opt);
    })
    taskStatus.value = status;

    taskDiv.appendChild(taskHeader);
    taskDiv.appendChild(taskStatus)
    return taskDiv
}

function generateTaskDropdown() {

}

export default function generateTasksList(tasks) {
    const tasksListDiv = document.createElement("DIV");
    tasksListDiv.className = "tasks-list";
    tasks.map(task => {
        const generatedTask = generateTask(task);
        tasksListDiv.appendChild(generatedTask);
    })
    return tasksListDiv
}

