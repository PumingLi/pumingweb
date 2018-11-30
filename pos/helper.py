import numpy as np
from math import log, factorial
from django.conf import settings
import pickle

class Viterbi:

    def __init__(self, alpha=0.005):

        with open(settings.STATIC_ROOT + 'pos/count_pos.pkl', 'rb') as f:
            self.count_pos = pickle.load(f)
        with open(settings.STATIC_ROOT + 'pos/emissions.pkl', 'rb') as f:
            self.emissions = pickle.load(f)
        with open(settings.STATIC_ROOT + 'pos/transition.pkl', 'rb') as f:
            self.transition = pickle.load(f)
        with open(settings.STATIC_ROOT + 'pos/initial.pkl', 'rb') as f:
            self.initial = pickle.load(f)
        self.alpha = alpha


    def read_input(self,input):
        test_set = []
        test_sentence = []
        word = ''
        for c in input:

            if c.isalnum():
                word += c
            else:
                if c == ' ':
                    if word:
                        test_sentence.append(word)
                    word = ''
                elif c == '.':
                    if word in ['Mr', 'Mrs', 'Ms', 'Miss']:
                        word += c
                    else:
                        if word:
                            test_sentence.append(word)
                        test_sentence.append(c)
                        test_set.append(test_sentence)
                        test_sentence = []
                        word = ''
                elif c == '-':
                    word += c
                else:
                    if word:
                        test_sentence.append(word)
                    test_sentence.append(c)
                    word = ''
        return test_set


    def predict(self, sentence):

        unique_pos = list(self.count_pos.keys())
        length_pos = len(unique_pos)

        trellis = np.zeros((length_pos, len(sentence)))
        back_pointers = np.zeros((length_pos, len(sentence)))

        # if sentence empty return empty path
        if not sentence:
            return []

        for j, word in enumerate(sentence):
            for i, pos in enumerate(unique_pos):

                cur_emission = self.emissions[pos][word] if word in self.emissions[pos] else 0
                uniques = len(self.emissions[pos])
                P_e = log((cur_emission + self.alpha)/(self.count_pos[pos] + self.alpha*(uniques+1)))


                if j == 0:
                    cur_pos = self.initial[pos]
                    total_pos = sum(self.initial.values())
                    uniques = len(self.initial.keys())
                    P_i = log((cur_pos + self.alpha)/(total_pos + self.alpha*(uniques+1)))


                    # On time zero, initialize first word with P_i
                    trellis[i][0] = P_i + P_e
                    back_pointers[i][0] = 0

                else:
                    max_prob = -1*float("inf")
                    max_idx = 0

                    # Find the previous path to maximize probability to current word
                    for k, p_pos in enumerate(unique_pos):
                        occur_pos = self.transition[p_pos][pos] if pos in self.transition[p_pos] else 0
                        total_pos = sum(self.transition[p_pos].values())
                        uniques = len(self.transition[p_pos])
                        P_t = log((occur_pos + self.alpha)/(total_pos + self.alpha*(uniques+1)))

                        if P_t + P_e + trellis[k][j-1] > max_prob:
                            max_idx = k
                            max_prob = P_t + P_e + trellis[k][j-1]

                    # Set value in trellis to max probability
                    trellis[i][j] = max_prob
                    back_pointers[i][j] = max_idx


        max_prob = -1*float("inf")
        max_path = []
        max_idx = 0

        # Find max probability at last word
        for k, pos in enumerate(unique_pos):
            if trellis[k][len(sentence)-1] > max_prob:
                max_idx = k
                max_prob = trellis[k][len(sentence)-1]
        max_path.append(max_idx)

        # Iterate backwards to find max path
        for x in range(len(sentence)-1, 0, -1):
            max_idx = int(back_pointers[max_idx][x])
            max_path.append(max_idx)

        prediction = list(zip(sentence, [unique_pos[i] for i in max_path[::-1]]))
        return prediction
