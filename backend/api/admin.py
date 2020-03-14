from django.contrib import admin

from .models import Project, Task


class ProjectAdmin(admin.ModelAdmin):
    # This tells Django to automatically fill in the `slug` field by slugifying the
    # `name` field.
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task)
