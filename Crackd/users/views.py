from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .forms import LoginForm, RegistrationForm

def loginView(request):

    if request.user.is_authenticated:
        return redirect('home')
        
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        targetUser = loginCheck(request)
        if targetUser != None:
          
            # Login User #
            user_login(request, targetUser)
            
            return redirect(request.GET.get('next', 'home'))
            
        else:
            messages.warning(request, f'Incorrect Username/Password.')
            
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

def loginCheck(request):

    # Check If Username Exists #
    inputUser = request.POST['username']
    targetUserList = User.objects.filter(username__iexact=inputUser)
    if len(targetUserList) == 1:
        
        # Check Username/Password #
        targetUser = authenticate(request, username=targetUserList.first().username, password=request.POST['password'])
        if targetUser != None:
            return targetUser
        
    return None

def logoutView(request):

    if request.user.is_authenticated:
        
        # Delete Generate Item Task #
        targetTask = PeriodicTask.objects.filter(name=f'Generate Item Process-' + request.user.username).first()
        if targetTask != None:
            targetTask.delete()
        
        # Logout User #
        user_logout(request)

    form = LoginForm()

    return redirect('login')

def registerView(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if registerCheck(request):
            
                # Create New User #
                targetUser = User.objects.create_user(username=request.POST['username'],
                                                      password=request.POST['password'],
                                                      email=request.POST['email'])
            
                # Login User #
                user_login(request, targetUser)
                return redirect('home')
    
    else:
        form = RegistrationForm()
        
    return render(request, 'users/register.html', {'form': form})
    
def registerCheck(request):

    check = True

    # Check If Username Exists #
    inputUser = request.POST['username']
    targetUserList = User.objects.filter(username__iexact=inputUser)
    if len(targetUserList) >= 1:
        messages.warning(request, f'Username already exists.')
        check = False
        
    # Check If Passwords Match #
    if request.POST['password'] != request.POST['passwordVerify']:
        messages.warning(request, f'Passwords do not match.')
        check = False
        
    # Check If Email Exists #
    inputEmail = request.POST['email']
    targetUserEmailList = User.objects.filter(email__iexact=inputEmail)
    if len(targetUserEmailList) >= 1:
        messages.warning(request, f'Email already exists.')
        check = False
        
    return check
