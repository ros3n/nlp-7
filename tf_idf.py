# -*- encoding: utf-8 -*-

from collections import defaultdict
import math
from helpers import *


class TfIdf(object):
    def __init__(self, library, dictionary):
        self.library = library
        self.dictionary = dictionary
        self.n = len(library)

    def tf(self, term, document):
        return document[1][term]

    def df(self, term):
        return sum([1 for d in self.library if d[1][term] > 0])

    def calculate_matrix(self):
        self.matrix = []
        for document in self.library:
            row = defaultdict(lambda: 0.0)
            for term in self.dictionary:
                w = self.weight(term, document)
                if w > 0:
                    row[term] = w
            self.matrix.append(row)
        return self.matrix

    def weight(self, term, document):
        return self.tf(term, document) * math.log(self.n / self.df(term))


if __name__ == '__main__':
    dictionary, library = load_library(
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    )
    tf_idf = TfIdf(library, dictionary)
