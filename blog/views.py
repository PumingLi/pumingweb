from django.shortcuts import render
from .models import Review

def blog(request):

    context = {'all_reviews': Review.objects.all}

    return render(request, 'blog.html', context=context)
