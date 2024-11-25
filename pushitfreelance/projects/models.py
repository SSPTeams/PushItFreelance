from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    employer = models.ForeignKey("users.EmployerProfile", on_delete=models.SET_NULL, blank=True, null=True)
    employee = models.ForeignKey("users.EmployeeProfile", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title
