from django.shortcuts import render

# Create your views here.
def bayes(request):
    return render(request, 'bayes.html')
