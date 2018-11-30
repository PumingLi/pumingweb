from django.shortcuts import render
from .forms import TaggerForm
from .helper import Viterbi
# Create your views here.
def tagger(request):
    return render(request, 'tagger.html')

def tag_input(request, input):
    # print(input)

    v = Viterbi()
    predictions = [v.predict(sentence) for sentence in v.read_input(input)]
    print(predictions)
    return render(request, 'predictions.html', context={"predictions":predictions})
