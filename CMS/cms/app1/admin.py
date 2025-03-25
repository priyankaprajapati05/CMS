from django.contrib import admin

from .models import Complaint, Profile, ResolvedComplaint

from .models import Complaint, ResolvedComplaint

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'complaint_type', 'device_type', 'specific_device', 'status', 'user', 'date_created')
    list_filter = ('status', 'device_type')
    search_fields = ('complaint_type', 'description', 'user__username')
    ordering = ('-date_created',)

admin.site.register(Complaint, ComplaintAdmin)

class ResolvedComplaintAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'resolved_date', 'resolution_notes', 'user')
    search_fields = ('complaint__complaint_type', 'resolution_notes', 'user__username')

admin.site.register(ResolvedComplaint, ResolvedComplaintAdmin)

admin.site.register(Profile)
