from django.shortcuts import render, redirect
from .forms import CommentForm
from .models import Review, Comment
from datetime import date


def blog(request):

    context = {'all_reviews': list(Review.objects.all())[::-1]}

    return render(request, 'blog.html', context=context)

def post(request, id):

    post = Review.objects.get(id=id)
    days_past = (date.today() - post.date).days
    days_past = "{} Days Ago".format(days_past) if days_past != 0 else "Today"
    context = {'review': post, 'delta': days_past, 'comments': post.comment_set, 'form': CommentForm()}

    return render(request, 'post.html', context=context)

def vote(request, id, vote):

    post = Review.objects.get(id=id)
    post.score += 1 if vote == "up" else -1
    post.save()
    context = {'review': post}
    return render(request, 'score.html', context=context)

def add_comment(request, id):

    post = Review.objects.get(id=id)
    f = CommentForm(request.POST)
    if f.is_valid():
        review = Comment(review=post,
                        name=f.cleaned_data['name'],
                        comment=f.cleaned_data['comment'],
                        score=0)
        review.save()
    return redirect('post', id=id)
