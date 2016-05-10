# -*- encoding: utf-8 -*-

from collections import Counter
import os.path
import pickle


def load_texts(path):
    text = ''
    with open(path) as f:
        text = f.read()
    return text.split('#')


def load_base_forms(bforms_dir, name_template, count):
    base_forms = []
    for i in range(count - 1):
        with open(os.path.join(bforms_dir, name_template.format(i)), 'rb') as f:
            data = pickle.load(f)
            base_forms.append(Counter(data))
    return base_forms


def get_dictionary(bforms):
    words = []
    for bf in bforms:
        words.extend(bf.keys())
    return list(set(words))


def load_library(texts_path, bforms_dir, name_template, count):
    texts = load_texts(texts_path)
    bforms = load_base_forms(bforms_dir, name_template, count)
    dictionary = get_dictionary(bforms)
    return dictionary, zip(texts, bforms)
