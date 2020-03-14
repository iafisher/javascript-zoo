import json
from django.test import TestCase
from django.urls import reverse

from .models import Project, Task


class ApiTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="test project", description="Lorem ipsum"
        )
        self.task = Task.objects.create(
            short_description="short description",
            long_description="long description",
            project=self.project,
            parent=None,
            order=0,
            status=Task.STATUS_PENDING,
        )

    def test_task_create(self):
        payload = {
            "description": "Update algorithm\n\nNeed to change docs too",
            "parent_pk": None,
            "project_pk": self.project.pk,
            "order": 0,
        }
        response = self._post_json("create_task", payload)
        self.assertEqual(list(response.keys()), ["pk"])
        task = Task.objects.get(pk=response["pk"])
        self.assertEqual(task.short_description, "Update algorithm")
        self.assertEqual(task.long_description, "Need to change docs too")
        self.assertEqual(task.project, self.project)
        self.assertEqual(task.status, task.STATUS_PENDING)
        self.assertEqual(task.order, 0)

    def test_task_update_description(self):
        payload = {"pk": self.task.pk, "description": "update_description text"}
        response = self._post_json(
            "update_task_description", payload, expecting={"pk": self.task.pk}
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.short_description, "update_description text")
        self.assertEqual(self.task.long_description, "")

    def test_task_update_status(self):
        payload = {"pk": self.task.pk, "status": Task.STATUS_COMPLETED}
        response = self._post_json(
            "update_task_status", payload, expecting={"pk": self.task.pk}
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.STATUS_COMPLETED)

    def test_task_delete(self):
        # Create a child task to make sure it is deleted as well.
        child_task = Task.objects.create(
            short_description="child short description",
            long_description="child long description",
            project=self.project,
            parent=self.task,
            order=0,
            status=Task.STATUS_PENDING,
        )
        payload = {"pk": self.task.pk}
        response = self._post_json(
            "delete_task", payload, expecting={"pk": self.task.pk}
        )
        self.assertEqual(Task.objects.filter(pk=self.task.pk).count(), 0)
        self.assertEqual(Task.objects.filter(pk=child_task.pk).count(), 0)

    def test_project_create(self):
        payload = {"name": "new project", "description": "project description"}
        response = self._post_json("create_project", payload)
        self.assertEqual(list(response.keys()), ["pk"])
        project = Project.objects.get(pk=response["pk"])
        self.assertEqual(project.name, "new project")
        self.assertEqual(project.description, "project description")

    def test_project_update_description(self):
        payload = {"pk": self.project.pk, "description": "new description"}
        response = self._post_json(
            "update_project_description", payload, expecting={"pk": self.project.pk}
        )
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "new description")

    def test_project_delete(self):
        payload = {"pk": self.project.pk}
        response = self._post_json(
            "delete_project", payload, expecting={"pk": self.project.pk}
        )
        self.assertEqual(Project.objects.filter(pk=self.project.pk).count(), 0)
        # A task under the project shouldn't be delete.
        self.assertEqual(Task.objects.filter(pk=self.task.pk).count(), 1)

    def _post_json(self, url, data, *, expecting=None, status_code=200):
        response = self.client.post(
            reverse(f"api:{url}"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status_code)
        response_as_json = json.loads(response.content)
        if expecting is not None:
            self.assertEqual(response_as_json, expecting)
        return response_as_json
