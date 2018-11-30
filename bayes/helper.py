import pickle
from django.conf import settings
from math import log

class Bayes:

    def __init__(self, alpha=0.005):
        with open(settings.STATIC_ROOT + 'bayes/spam_map.pkl', 'rb') as f:
            self.spam_map = pickle.load(f)
        with open(settings.STATIC_ROOT + 'bayes/ham_map.pkl', 'rb') as f:
            self.ham_map = pickle.load(f)
        with open(settings.STATIC_ROOT + 'bayes/total.pkl', 'rb') as f:
            self.total = pickle.load(f)
        self.alpha = alpha

    def read_input(self, input):
        test_set = []
        word = ''
        for c in input:

            if c.isalnum():
                word += c
            else:
                if c == ' ':
                    if word:
                        test_set.append(word)
                    word = ''
                elif c == '.':
                    if word in ['Mr', 'Mrs', 'Ms', 'Miss']:
                        word += c
                    else:
                        if word:
                            test_set.append(word)
                        test_set.append(c)
                        word = ''
                elif c == '-':
                    word += c
                else:
                    if word:
                        test_set.append(word)
                    test_set.append(c)
                    word = ''
        return test_set

    def predict(self, input):

        #SPAM
        n = sum(self.spam_map.values())
        V = len(self.total)
        spam_probs = {k: log((self.spam_map[k] + self.alpha)/(n + self.alpha*(V+1))) for k in self.spam_map}

        spam_prob = 0
        for w in input:
            if(w in spam_probs):
                spam_prob += spam_probs[w]
            else:
                spam_prob += log((self.alpha)/(n + self.alpha*(V+1)))

        #HAM
        n = sum(self.ham_map.values())
        V = len(self.total)
        ham_probs = {k: log((self.ham_map[k] + self.alpha)/(n + self.alpha*(V+1))) for k in self.ham_map}


        ham_prob = 0
        for w in input:
            if(w in ham_probs):
                ham_prob += ham_probs[w]
            else:
                ham_prob += log((self.alpha)/(n + self.alpha*(V+1)))

        return (ham_prob, spam_prob)
