# coding: utf-8

class StopWordRemover:
    def __init__(self, stopwords=[]):
        self.stopwords = stopwords or self.get_stopwords()


    def get_stopwords(self):
        f = open('stopwords.txt', 'r')
        stopwords = f.read().splitlines()
        return stopwords


    def remove_stopwords(self, text):
        result = []
        texts = text.split()
        for word in texts:
            if word not in self.stopwords:
                result.append(word)
        final = ' '.join(result)
        return final