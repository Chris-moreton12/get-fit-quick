from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm

@login_required
def comment_board(request):
    comments = Comment.objects.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('newsletter:comment_board')
    else:
        form = CommentForm()

    context = {
        'comments': comments,
        'form': form,
    }
    return render(request, 'newsletter/comment_board.html', context)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Only allow the comment owner to delete
    if comment.user == request.user:
        comment.delete()

    return redirect('newsletter:comment_board')
