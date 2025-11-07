from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm


def review_list(request):
    reviews = Review.objects.order_by('-created_at')
    return render(request, 'reviews/reviews.html', {'reviews': reviews})


@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been posted.")
            return redirect('reviews')
    else:
        form = ReviewForm()
    return render(request, 'reviews/add_review.html', {'form': form})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        messages.error(request, "You can only delete your own reviews.")
        return redirect('reviews')

    # Delete instantly on POST
    if request.method == 'POST':
        review.delete()
        messages.success(request, "Your review has been deleted.")
    return redirect('reviews')
