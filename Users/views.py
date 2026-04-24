from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import*

# user registration viewfrom django.shortcuts import render, redirect


def register(request):
    if request.method == 'POST':
        form = FarmUserForm(request.POST)
        if form.is_valid():
            # The .save() method in your form already handles set_password()
            user = form.save()
            
            # Show success message
            messages.success(request, f"Welcome, {user.username}! Your farm account has been created.")
            
            # Automatically log the user in
            login(request, user)
            
            # Redirect to the farm dashboard or crop list
            return redirect('Login') 
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = FarmUserForm()
    
    return render(request, 'register.html', {'form': form})
 # user login view


def Login(request):
    if request.method == 'POST':
        form = FarmLoginForm(request.POST)
        if form.is_valid():
            u_name = form.cleaned_data.get('username')
            p_word = form.cleaned_data.get('password')
            
            user = authenticate(request, username=u_name, password=p_word)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back to the farm, {u_name}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = FarmLoginForm()
    
    return render(request, 'login.html', {'form': form})
