from mferp.auth.user.models import Account
from django.db import models

class Employee(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    # Add other fields specific to the Employee model
    employee_code = models.CharField(max_length=10)
    hire_date = models.DateField()
    # Add more fields as needed

    def __str__(self):
        return self.user.email  