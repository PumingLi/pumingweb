from django.shortcuts import render

def diet(request):
    return render(request, 'diet.html')
