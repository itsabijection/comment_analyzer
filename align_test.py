from scipy.spatial import distance
import align

def test(m1, m2):
    unaligned=[]
    aligned=[]
    vocab_obj, _ = align.intersect(m1,m2)
    for w in vocab_obj.wv.vocab:
        unaligned.append(distance.cosine(m1.wv[w], m2.wv[w]))
    m2=align.procrustes(m1,m2)
    for w in vocab_obj.wv.vocab:
        aligned.append(distance.cosine(m1.wv[w], m2.wv[w]))
    return unaligned, aligned