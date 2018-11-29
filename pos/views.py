from django.shortcuts import render
from .forms import TaggerForm
# Create your views here.
def tagger(request):

    return render(request, 'tagger.html', context={'form': TaggerForm()})
