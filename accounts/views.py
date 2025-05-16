from django.shortcuts import render, redirect
from .forms import ContactForm  # Import the ContactForm
from django.contrib.auth.forms import UserCreationForm

# Signup view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

# Contact view for the contact page
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # After successful form submission, redirect to the thank_you page
            return redirect('thank_you')  # This redirects to the 'thank_you'
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

# Thank you view (for after form submission)
def thank_you(request):
    return render(request, 'thank_you.html')  # This will render the 'thank_you.html' template

