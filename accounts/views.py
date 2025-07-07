from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import ContactForm, CustomUserCreationForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save to database
            messages.success(request, "Thank you! Your message has been sent.")
            return redirect('thank_you')  # Redirect to thank you page
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def thank_you(request):
    return render(request, 'thank_you.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log user in after signup
            messages.success(request, "Account created successfully.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

