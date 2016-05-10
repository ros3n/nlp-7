# -*- encoding: utf-8 -*-

import re
import sys


def preprocess(file_in, file_out):
    data = None
    with open(file_in) as f:
        data = f.read().lower()
    data = re.sub(r'#\d{6}', '#', data)
    data = re.sub(r'[\.|,|\-|_|\!|\?|;|"|\(|\)]', ' ', data)
    data = re.sub(r'[^a-z|ą|ć|ę|ł|ń|ó|ś|ż|ź|\n|\s|#|0-9]', '', data)
    # data = re.sub(r'\n+', ' ', data)
    data = re.sub(r'\s+', ' ', data)
    with open(file_out, 'w') as f:
        f.write(data)


if __name__ == '__main__':
    preprocess(sys.argv[1], sys.argv[2])
