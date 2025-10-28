from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import EmployeeManager


class Employee(AbstractBaseUser, PermissionsMixin):
    DEPARTMENT_CHOICES = [
        ('HR', 'Human Resources'),
        ('IT', 'Information Technology'),
        ('Finance', 'Finance'),
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('Operations', 'Operations'),
    ]

    DESIGNATION_CHOICES = [
        ('Manager', 'Manager'),
        ('Senior Developer', 'Senior Developer'),
        ('Developer', 'Developer'),
        ('Junior Developer', 'Junior Developer'),
        ('HR Executive', 'HR Executive'),
        ('Accountant', 'Accountant'),
        ('Sales Executive', 'Sales Executive'),
        ('Marketing Executive', 'Marketing Executive'),
    ]

    employee_id = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    designation = models.CharField(max_length=30, choices=DESIGNATION_CHOICES)
    date_of_joining = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_hr = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'employee_id']

    class Meta:
        db_table = 'employees'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
