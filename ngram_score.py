'''
ngram_score.py -> Ngram scoring class
'''

from math import log10

class NgramScore(object):
    def __init__(self, ngramfile, sep=' '):
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}
        total = 0
        try:
            with open(ngramfile, 'r') as f:
                for line in f:
                    key, count = line.split(sep)
                    self.ngrams[key] = int(count)
                    total += int(count)
        except IOError:
            print(f"Error: Could not read {ngramfile}")
            print("Please ensure 'english_quadgrams.txt' is in the same directory.")
            # Fallback/Dummy data to prevent crash if file missing, though score will be useless
            self.ngrams = {'TION': 1000, 'NTHE': 900, 'THER': 800, 'THAT': 700, 'OFTH': 600} 
            total = sum(self.ngrams.values())

        self.L = len(list(self.ngrams.keys())[0])
        self.N = total
        # calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key])/self.N)
        self.floor = log10(0.01/self.N)

    def score(self, text):
        ''' compute the score of text '''
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text)-self.L+1):
            if text[i:i+self.L] in self.ngrams:
                score += ngrams(text[i:i+self.L])
            else:
                score += self.floor
        return score
