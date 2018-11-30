from django.shortcuts import render
from .helper import Bayes

# Create your views here.
def bayes(request):
    return render(request, 'bayes.html')

def classify_input(request, input):

    bayes = Bayes()
    input_set = bayes.read_input(input)
    prediction = bayes.predict(input_set)
    print(prediction)
    context = {'ham_prob':"{0:.2f}".format(prediction[0]), 'spam_prob':"{0:.2f}".format(prediction[1]), "is_spam": prediction[0] < prediction[1]}
    return render(request, 'email_prediction.html', context=context)
