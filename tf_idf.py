# -*- encoding: utf-8 -*-

from collections import defaultdict
import math
import pickle
import dill
import sys
from helpers import *


class TfIdf(object):
    def __init__(self, library, dictionary):
        self.library = library
        self.dictionary = dictionary
        self.n = len(library)
        self.df_dict = {}

    def tf(self, term, document):
        return document[1][term]

    def calculate_df(self, term):
        return sum([1 for d in self.library if d[1][term] > 0])

    def calculate_dfs(self):
        for i, term in enumerate(self.dictionary):
            print i
            self.df_dict[term] = self.calculate_df(term)

    def df(self, term):
        return self.df_dict[term]

    def calculate_matrix(self):
        self.matrix = []
        for i, document in enumerate(self.library):
            print i
            row = defaultdict(lambda: 0.0)
            for term in document[1].keys():
                w = self.weight(term, document)
                if w > 0:
                    row[term] = w
            self.matrix.append(row)
        return self.matrix

    def weight(self, term, document):
        return self.tf(term, document) * math.log(self.n / self.df(term))

    def get_text(self, index):
        print self.library[index][0]

    def get_keywords(self, index, n):
        data = self.matrix[index].items()
        data = list(reversed(sorted(data, key=lambda x: x[1])))
        for d in data[:n]:
            print u'({0}, {1})'.format(d[0], d[1]),


# if __name__ == '__main__':
# dictionary, library = load_library(
    # sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
# )
dictionary, library = load_library(
    'pap.txt', 'forms', 'forms{0}.data', 51575
)
tf_idf = TfIdf(library, dictionary)
with open('df.data', 'rb') as f:
    tf_idf.df_dict = pickle.load(f)
with open('matrix.data', 'rb') as f:
    tf_idf.matrix = pickle.load(f)
