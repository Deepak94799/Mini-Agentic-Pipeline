from src.planner import Planner
import json, os
p = Planner()
queries = json.load(open('../tests/test_queries.json'))
os.makedirs('../outputs', exist_ok=True)
notes = []
for q in queries:
    out = p.handle(q['query'])
    note = {'id': q.get('id'), 'query': q.get('query'), 'final_answer': out.get('final_answer'), 'tool_used': any(s.get('step')=='actor_call' for s in out.get('steps',[]))}
    notes.append(note)
json.dump(notes, open('../outputs/evaluation_notes.json','w'), indent=2)
print('Wrote outputs/evaluation_notes.json')