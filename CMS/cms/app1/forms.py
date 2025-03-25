from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['complaint_type', 'device_type', 'specific_device', 'description']
 

class AdminUpdateStatusForm(forms.Form):
    status = forms.ChoiceField(choices=[
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('not_resolved', 'Not Resolved')
    ])
