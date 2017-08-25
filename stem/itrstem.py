# encoding: utf-8
from six import python_2_unicode_compatible
from np_lang.stem.api import Stemmer


@python_2_unicode_compatible
class IterativeStemmer(Stemmer):
    def __init__(self):
        self.category_1 = self.read_file('category_1.txt')
        self.category_2 = self.read_file('category_2.txt')
        self.category_3 = self.read_file('category_3.txt')

    def read_file(self, filename):
        f = open(filename, 'r', encoding='utf-8')
        rule = f.read().splitlines()
        return rule

    def stem(self, word):
        result = self.remove_category_1(word)
        return self.remove_category_2(result)

    def remove_category_1(self, word):
        for rule in self.category_1:
            if word.endswith(rule):
                return word[:-len(rule)]
                break
        return word

    def remove_category_3(self, word):
        for rule in self.category_3:
            if word.endswith(rule):
                return word[:-len(rule)], True
                break
        return word, False

    def remove_category_2(self, word):
        if word.endswith(tuple(self.category_2)):
            if word.endswith("ँ") or word.endswith("ं"):
                if word[:-1].endswith(("ो", "ु", "उ", "े", "ोै")):
                    return self.remove_category_2(word[:-1])
                else:
                    return word
            elif word.endswith("ै"):
                if word[:-1].endswith("त्र"):
                    return self.remove_category_2(word[:-1])
                else:
                    return word
            else:
                return self.remove_category_2(word[:-1])

        result, success = self.remove_category_3(word)
        if success:
            return self.remove_category_2(result)
        return result