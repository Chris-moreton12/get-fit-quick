from django.shortcuts import render, redirect
from .forms import ContactForm, CustomUserCreationForm  # Import the custom user creation form and contact form

# Signup view
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use custom form with email required
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = CustomUserCreationForm()

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
