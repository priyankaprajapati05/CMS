# models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    division = models.CharField(max_length=100)  # Remove default and allow blank=False
    designation = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username


from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):
    PENDING = 'Pending'
    RESOLVED = 'Resolved'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (RESOLVED, 'Resolved'),
    ]

    complaint_type = models.CharField(max_length=100)
    device_type = models.CharField(max_length=100)
    specific_device = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PENDING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.complaint_type}'
    
# Ensure User model has `name` and `employee_id` fields
User.add_to_class('employee_id', models.CharField(max_length=10, blank=True, null=True))
User.add_to_class('name', models.CharField(max_length=100, blank=True, null=True))

class ResolvedComplaint(models.Model):
    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE)  # Link to Complaint
    complaint_type = models.CharField(max_length=100)
    device_type = models.CharField(max_length=100)
    specific_device = models.CharField(max_length=100)
    description = models.TextField()
    resolution_notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=Complaint.STATUS_CHOICES)
    resolved_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resolved_complaints')  # Ensure user field is correct

    def __str__(self):
        return f"{self.complaint_type} - {self.device_type} - {self.user.username}"
  