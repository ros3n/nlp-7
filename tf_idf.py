# -*- encoding: utf-8 -*-

from collections import defaultdict
import heapq
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
        return self.df_dict.get(term) or self.n

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

    def query(self, query_string):
        terms = query_string.lower().split()
        query_weights = self.query_weights(terms)
        results = []
        for i, doc in enumerate(self.matrix):
            d = self.calculate_distance(query_weights, doc)
            if len(results) <= 10:
                heapq.heappush(results, (d, i))
            else:
                heapq.heappushpop(results, (d, i))
        return list(reversed(sorted(results, key=lambda x: x[0])))

    def calculate_distance(self, v1, v2):
        keys = set(v1.keys()) & set(v2.keys())
        v1_len = math.sqrt(sum([v**2 for v in v1.values()]))
        v2_len = math.sqrt(sum([v**2 for v in v2.values()]))
        if v1_len * v2_len == 0:
            return 0.0
        prod = sum([v1[k] * v2[k] for k in keys])
        return prod / (v1_len * v2_len)

    def query_weights(self, terms):
        tfs = Counter(terms)
        max_tf = tfs.most_common()[0][1]
        return {t: self.query_weight(t, tfs[t], max_tf) for t in terms}

    def query_weight(self, term, tf, max_tf):
        return (0.5 + 0.5 * tf / max_tf) * math.log(self.n / self.df(term))

    def similar(self, doc_id):
        sample = self.matrix[doc_id]
        results = []
        for i, doc in enumerate(self.matrix):
            if i == doc_id:
                continue
            d = self.calculate_distance(sample, doc)
            if len(results) <= 10:
                heapq.heappush(results, (d, i))
            else:
                heapq.heappushpop(results, (d, i))
        return list(reversed(sorted(results, key=lambda x: x[0])))


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
reload(sys)
sys.setdefaultencoding('utf-8')
