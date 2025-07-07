from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages

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
