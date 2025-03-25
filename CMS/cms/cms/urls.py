# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app1 import views
 
urlpatterns = [
    path('', views.LoginPage, name='login'),
    path('admin/', admin.site.urls),
    path('signup/', views.SignupPage, name='signup'),
    path('home/', views.HomePage, name='home'),
    path('new_complaint/', views.NewComplaintPage, name='new_complaint'),
    path('profile/', views.ProfilePage, name='profile'),
    path('complaint_status/', views.complaint_status, name='complaint_status'),
    path('logout/', views.LogoutPage, name='logout'),

    path('resolved_complaints/', views.resolved_complaints, name='resolved_complaints'),
    path('admin_update_status/<int:complaint_id>/', views.admin_update_status, name='admin_update_status'),
    path('admin_login/', views.AdminLoginPage, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.admin_logout, name='logout'),
]



# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)