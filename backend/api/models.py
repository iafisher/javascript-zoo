from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    name = models.CharField(max_length=50)
    # "A slug is a short label for something, containing only letters, numbers,
    # underscores or hyphens. They're generally used in URLs."
    # (https://docs.djangoproject.com/en/3.0/ref/models/fields/#slugfield)
    slug = models.SlugField(max_length=50)
    description = models.TextField()
    archived = models.BooleanField(default=False)
    # `auto_now_add=True` tells Django to set this field to the current time when the
    # object is created.
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def json(self):
        top_level_tasks = Task.objects.filter(project=self, parent=None)
        tasks_json = [task.json() for task in top_level_tasks.order_by("order")]
        return {
            "id": self.pk,
            "name": self.name,
            "description": self.description,
            "archived": self.archived,
            "tasks": tasks_json,
        }

    def __str__(self):
        return self.name


class Task(models.Model):
    short_description = models.CharField(max_length=100)
    long_description = models.TextField(blank=True)
    # `on_delete=models.SET_NULL` tells Django that when a Task object's Project is
    # deleted, the `project` field should be set to null (instead of, for instance,
    # deleting the Task object as well). This is a safer setting that reduces the risk
    # of accidental data loss.
    project = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    # The order of the task under its parent task.
    order = models.PositiveSmallIntegerField(default=0)
    # The Django idiom for a "multiple-choice" field is very verbose.
    STATUS_PENDING = "pending"
    STATUS_COMPLETED = "completed"
    STATUS_BLOCKED = "blocked"
    STATUS_NON_BLOCKING = "non-blocking"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        # The first element in each pair is the actual value Django stores in the
        # database, and the second element is the human-readable value. In our case,
        # we store the human-readable value directly in the database.
        (STATUS_PENDING, STATUS_PENDING),
        (STATUS_COMPLETED, STATUS_COMPLETED),
        (STATUS_BLOCKED, STATUS_BLOCKED),
        (STATUS_NON_BLOCKING, STATUS_NON_BLOCKING),
        (STATUS_FAILED, STATUS_FAILED),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # `auto_now=True` tells Django to set this field to the current time whenever the
    # object is changed.
    last_updated = models.DateTimeField(auto_now=True)

    def json(self):
        children = Task.objects.filter(parent=self)
        children_json = [task.json() for task in children.order_by("order")]
        return {
            "id": self.pk,
            "shortDescription": self.short_description,
            "longDescription": self.long_description,
            "projectId": self.project.pk,
            "parentId": self.parent.pk if self.parent else None,
            "order": self.order,
            "status": self.status,
        }

    def __str__(self):
        return f"[{self.project}] {self.short_description}"


def delete_task_recursively(task):
    """Deletes a task and all its subtasks and all their subtasks and so on."""
    for subtask in task.task_set.all():
        delete_task_recursively(subtask)

    task.delete()
