from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

# User, AbstractUser, AbstractBaseUser


class User(AbstractUser):
    telegram_id = models.CharField(max_length=255, blank=True, null=True)


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

        '''
        constraints = [
            models.CheckConstraint(
                check=models.Q(salary__gte=0),
                name="salary_gte_0",
            )
        ]
        '''


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Employer"
        verbose_name_plural = "Employers"
