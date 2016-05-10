import gc
import pickle
import imp
import sys


def plp_bforms(PLP, inp=sys.stdin):
    data = inp.read()
    documents = data.split('#')
    p = PLP()
    for j, d in enumerate(documents):
        gc.collect()
        data = d.split()
        ids = []
        nids = []
        for w in data:
            i = plp_id(w, p)
            ids.append(i) if i else nids.append(w)
        bforms = [p.bform(i) for i in ids]
        bforms.extend(nids)
        with open('/home/pjn2016/rrozak/forms{0}.data'.format(j), 'wb') as f:
            pickle.dump(bforms, f)


def plp_id(word, plp):
    rec = plp.rec(word)
    return rec[0] if rec else None


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    plp = imp.load_source('plp', '/usr/local/plp/plp.py')
    data = plp_bforms(plp.PLP)
    with open('/home/pjn2016/rrozak/forms2.data', 'wb') as f:
        pickle.dump(data, f)

if __name__ == '__main__':
    main()
