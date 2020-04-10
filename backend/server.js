const express = require('express');
const path = require('path');
const sequelize = require('sequelize');
const db = require('./models');

const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.get('/vanilla', (req, res) => {
  res.sendFile('vanilla.html', { root: path.join(__dirname, 'views') });
});

app.get('/svelte', (req, res) => {
  res.sendFile('svelte.html', { root: path.join(__dirname, 'views') });
});

app.get('/api/project/get', (req, res) => {
  const projectId = req.query.id;
  db.Project.findAll({ where: { id: projectId }})
    .then(projects => {
      return projectToFrontendJson(projects[0])
    }).then(project => {
      res.send(project)
    });
});

app.post('/api/task/create', (req, res) => {
  const { description, order, parentId, projectId } = req.body;
  return db.Task.create({
    shortDescription: description,
    longDescription: "",
    order,
    projectId,
    parentId,
    status: "pending",
  }).then(task => {
    res.json(task)
  });
});

app.post('/api/task/update/status', (req, res) => {
  const { id, status } = req.body;
  db.Task.update({ status }, { where: { id }}).then(task => {
    res.json(task);
  });
});

/**
 * Convert the `project` object into the JSON format the frontend expects.
 *
 * Mainly this means recursively finding all of the tasks under the project and putting
 * them in a tree structure
 */
function projectToFrontendJson(project) {
  return db.Task.findAll({
    where: { projectId: project.id, parentId: null },
    order: sequelize.col('order'),
  }).then(tasks => {
    return Promise.all(tasks.map(taskToFrontendJson));
  }).then(tasksJson => {
    return {
      id: project.id,
      name: project.name,
      description: project.description,
      archived: project.archived,
      tasks: tasksJson,
    }
  });
}

/**
 * Convert the `task` object into the JSON format the frontend expects.
 *
 * Mainly this means recursively finding all of its subtasks and putting them in a tree
 * structure.
 */
function taskToFrontendJson(task) {
  return db.Task.findAll({
    where: { parentId: task.id },
    order: sequelize.col('order'),
  }).then(tasks => {
    return Promise.all(tasks.map(taskToFrontendJson));
  }).then(tasksJson => {
    return {
      id: task.id,
      shortDescription: task.shortDescription,
      longDescription: task.longDescription,
      projectId: task.projectId,
      parentId: task.parentId,
      order: task.order,
      status: task.status,
    };
  });
}

app.listen(port, () => console.log('Listening at http://localhost:' + port));
