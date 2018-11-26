import pandas as pd


class Viterbi:

    def __init__(self):
        self.count_df = pd.Series.from_csv('training/count_df.csv')
        self.emission_df = pd.DataFrame.from_csv('training/emission_df.csv')
        self.transition_df = pd.DataFrame.from_csv('training/transition_df.csv')
        self.initial_df = pd.Series.from_csv('training/initial_df.csv')
