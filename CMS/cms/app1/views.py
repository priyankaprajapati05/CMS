# views.py

from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ComplaintForm,AdminUpdateStatusForm
from .models import Complaint, Profile , ResolvedComplaint
from datetime import datetime
from django.utils import timezone


def LoginPage(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')

        # Authenticate user using Employee ID as username
        user = authenticate(request, username=employee_id, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Invalid Employee ID or Password.")

    return render(request, 'login.html')


def SignupPage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        employee_id = request.POST.get('employee_id')
        division = request.POST.get('division')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate the form data
        if not all([name, employee_id, division, password1, password2]):
            messages.error(request, "All fields are required.")
            return render(request, 'signup.html')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        # Additional validation and user creation
        try:
            user = User.objects.create_user(username=employee_id, password=password1)
            user.first_name = name
            user.save()

            # Create a profile for the user
            profile = Profile.objects.create(user=user, division=division)
            profile.save()

        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")
            return render(request, 'signup.html')

        messages.success(request, "Your account has been created successfully.")
        return redirect('login')

    return render(request, 'signup.html')

@login_required(login_url='login')
def NewComplaintPage(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return redirect('complaint_status')
        else:
            print(form.errors)  # Check for any form validation errors
    else:
        form = ComplaintForm()
    return render(request, 'new_complaint.html', {'form': form})

@login_required(login_url='login')
def ProfilePage(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile.division = request.POST.get('division', profile.division)
        profile.designation = request.POST.get('designation', profile.designation)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        user.first_name = request.POST.get('name', user.first_name)
        user.email = request.POST.get('email', user.email)
        user.current_date = datetime.now().strftime('%d-%m-%Y')
        profile.save()
        user.save()

        # Add success message
        messages.success(request, 'PROFILE UPDATED SUCCESSFULLY')

        # Redirect to profile page to avoid form resubmission on refresh
        return redirect('profile')  # Replace 'profile' with your actual profile URL name
        
    return render(request, 'profile.html', {'user': user, 'profile': profile})

@login_required(login_url='login')
def HomePage(request):
    current_date = datetime.now().strftime('%d-%m-%Y')
    user = request.user
    context = {
        'current_date': current_date,
        'user': user,
        'name': user.first_name,  # Assuming name is used for name
        'employee_id': user.username,  # Assuming username (default field) is used for employee_id
    }
    return render(request, 'home.html', context)


@login_required(login_url='login')
def complaint_status(request):
    user_complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'complaint_status.html', {'user_complaints': user_complaints})

def LogoutPage(request):
    logout(request)
    return redirect('login')
 


def AdminLoginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user with Django's authentication system
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return HttpResponse("Invalid username or password.")

    return render(request, 'admin_login.html')


@login_required(login_url='admin_login')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    # Exclude complaints with status 'Resolved'
    complaints = Complaint.objects.exclude(status='Resolved')
    return render(request, 'admin_dashboard.html', {'complaints': complaints})



from django.db import IntegrityError

@login_required(login_url='admin_login')
def admin_update_status(request, complaint_id):
    if not request.user.is_staff:
        return redirect('home')
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        complaint.status = status
        complaint.save()

        if status == 'Resolved':
            # Move the complaint to ResolvedComplaint
            resolved_complaint, created = ResolvedComplaint.objects.get_or_create(
                complaint=complaint,
                defaults={
                    'resolution_notes': request.POST.get('resolution_notes', ''),
                    'user': request.user  # Ensure the `user` field is set
                }
            )
            if not created:
                resolved_complaint.resolution_notes = request.POST.get('resolution_notes', '')
                resolved_complaint.user = request.user
                resolved_complaint.save()

            # Log the creation or update of the resolved complaint
            print(f'ResolvedComplaint {"created" if created else "updated"}: {resolved_complaint}')
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')


@login_required(login_url='admin_login')
def resolved_complaints(request):
    resolved_complaints = ResolvedComplaint.objects.filter(complaint__status='Resolved')
    print(f'Retrieved Resolved Complaints: {resolved_complaints.count()}')  # Log the number of retrieved complaints
    return render(request, 'resolved_complaints.html', {'resolved_complaints': resolved_complaints})


from django.contrib.auth import logout as auth_logout

def admin_logout(request):
    auth_logout(request)
    return redirect('login')





