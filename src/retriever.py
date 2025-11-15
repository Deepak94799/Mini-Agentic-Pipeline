import os, time, json
from src.utils import get_api_key
try:
    import openai
except:
    openai = None
import math

class Retriever:
    def __init__(self, docs_path='docs'):
        self.docs = self._load_docs()
        self.use_embeddings = False
        self.emb_index = None
        key = get_api_key()
        if key and openai:
            try:
                openai.api_key = key
                # try to create embeddings for each doc (non-persistent in this simple retriever)
                texts = list(self.docs.values())
                resp = openai.Embeddings.create(input=texts, model='text-embedding-3-small')
                embs = [r['embedding'] for r in resp['data']]
                # normalize embs
                self.emb_index = dict(zip(list(self.docs.keys()), embs))
                self.use_embeddings = True
            except Exception as e:
                # embedding build failed; fall back to keyword
                self.use_embeddings = False

    def _load_docs(self):
        docs = {}
        for fn in sorted(os.listdir('docs')):
            p = os.path.join('docs', fn)
            if os.path.isfile(p):
                with open(p, 'r', encoding='utf-8') as f:
                    docs[fn] = f.read()
        return docs

    def _cosine(self, a, b):
        na = math.sqrt(sum(x*x for x in a))
        nb = math.sqrt(sum(x*x for x in b))
        if na==0 or nb==0: return 0.0
        return sum(x*y for x,y in zip(a,b))/(na*nb)

    def retrieve(self, query, top_k=3):
        start = time.time()
        if self.use_embeddings and self.emb_index:
            try:
                q_emb = openai.Embeddings.create(input=[query], model='text-embedding-3-small')['data'][0]['embedding']
                scores = []
                for k,v in self.emb_index.items():
                    scores.append((k, self._cosine(q_emb, v)))
                scores.sort(key=lambda x: x[1], reverse=True)
                hits = [{'doc_id':n, 'score':s, 'text': self.docs[n]} for n,s in scores[:top_k]]
                return {'method':'embeddings','hits':hits,'elapsed':time.time()-start}
            except Exception:
                pass
        # keyword fallback
        qtokens = set(query.lower().split())
        scores = []
        for name, text in self.docs.items():
            tks = set(text.lower().split())
            overlap = len(qtokens & tks)
            scores.append((name, overlap))
        scores.sort(key=lambda x: x[1], reverse=True)
        hits = [{'doc_id':n, 'score':s, 'text': self.docs[n]} for n,s in scores[:top_k]]
        return {'method':'keyword','hits':hits,'elapsed':time.time()-start}