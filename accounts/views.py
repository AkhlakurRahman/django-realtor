from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

# Create your views here.


def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if password match
        if password == password2:
            # Check if username exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken! Try another')
                return redirect('register')
            else:
                # Check if email exists
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already taken! Try another')
                    return redirect('register')
                else:
                    # Everything ok
                    user = User.objects.create_user(
                        first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                    # Save user to db
                    user.save()
                    messages.success(
                        request, 'You have registered, now you can log in!')
                    # Redirect to login page
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('index')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
