import os, json, time
from src.utils import get_api_key
try:
    import openai
except:
    openai = None

class Reasoner:
    def __init__(self, model='gpt-3.5-turbo', prompt_version='v2'):
        self.model = model
        self.prompt_version = prompt_version
        base = os.path.join(os.path.dirname(__file__), '..', 'prompts')
        self.templates = {}
        try:
            self.templates['v1'] = open(os.path.join(base, 'prompts_v1.txt')).read()
            self.templates['v2'] = open(os.path.join(base, 'prompts_v2.txt')).read()
            self.templates['v3'] = open(os.path.join(base, 'prompts_v3.txt')).read()
        except Exception:
            pass
        key = get_api_key()
        if key and openai:
            openai.api_key = key

    def decide(self, query, context):
        start = time.time()
        if openai is None or not getattr(openai, 'api_key', None):
            lowered = query.lower()
            if any(k in lowered for k in ['price','stock','lookup','in stock','how much','source_date']):
                return {'decision':'tool','reason':'heuristic detected numeric lookup','elapsed': time.time()-start}
            return {'decision':'kb','reason':'heuristic non-numeric','answer': context, 'elapsed': time.time()-start}
        prompt = self.templates.get(self.prompt_version, '').replace('{query}', query).replace('{context}', context)
        try:
            resp = openai.ChatCompletion.create(model=self.model, messages=[{'role':'system','content':'You are an agentic assistant.'},{'role':'user','content':prompt}], max_tokens=400)
            text = resp['choices'][0]['message']['content']
            try:
                j = json.loads(text)
                return {'decision':'llm','reason':'llm output','llm_json':j,'llm_text':text,'elapsed': time.time()-start}
            except Exception:
                return {'decision':'llm','reason':'llm raw','llm_text':text,'elapsed': time.time()-start}
        except Exception as e:
            return {'decision':'tool','reason':'llm failed','error':str(e),'elapsed': time.time()-start}
