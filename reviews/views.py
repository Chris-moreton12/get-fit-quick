from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

def review_list(request):
    reviews = Review.objects.order_by('-created_at')
    return render(request, 'reviews/reviews.html', {'reviews': reviews})

@login_required
def add_review(request):
    # Intentional error to test DEBUG = False
    raise Exception("Test error: checking if DEBUG mode is off")

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews')
    else:
        form = ReviewForm()
    return render(request, 'reviews/add_review.html', {'form': form})
