from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "employer", "employee", "budget", "deadline", "created_at", "updated_at"]
    list_filter = ["employer", "employee"]
    search_fields = ["title", "description"]


# Register your models here.
admin.site.register(Project, ProjectAdmin)

