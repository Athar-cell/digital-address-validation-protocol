# ml_similarity.py
import math
import re
from collections import Counter

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False

def simple_tokenize(s):
    s = (s or '').lower()
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    tokens = [t for t in s.split() if len(t) > 0]
    return tokens

def cosine_sim_tokens(a, b):
    ta = Counter(simple_tokenize(a))
    tb = Counter(simple_tokenize(b))
    all_tokens = set(ta.keys()) | set(tb.keys())
    va = [ta.get(t,0) for t in all_tokens]
    vb = [tb.get(t,0) for t in all_tokens]
    dot = sum(x*y for x,y in zip(va,vb))
    na = math.sqrt(sum(x*x for x in va))
    nb = math.sqrt(sum(x*x for x in vb))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

def similarity_score(a, b):
    a = a or ''
    b = b or ''
    if SKLEARN_AVAILABLE:
        try:
            vect = TfidfVectorizer().fit([a, b])
            X = vect.transform([a, b])
            sim = float(cosine_similarity(X[0], X[1])[0,0])
            return sim
        except Exception:
            return cosine_sim_tokens(a, b)
    else:
        return cosine_sim_tokens(a, b)
