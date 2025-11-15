from src.planner import Planner
import json, os, csv, time
p = Planner()
queries = json.load(open('tests/test_queries.json'))
results = []
os.makedirs('outputs', exist_ok=True)
latency_csv = open('outputs/latency_report.csv','w', newline='', encoding='utf-8')
writer = csv.writer(latency_csv)
writer.writerow(['id','query','retrieval','reasoner','actor','total'])
for q in queries:
    start = time.time()
    out = p.handle(q['query'])
    results.append(out)
    timings = out.get('timings',{})
    writer.writerow([q.get('id'), q.get('query'), timings.get('retrieval'), timings.get('reasoner'), timings.get('actor'), timings.get('total')])
    print(f"Q: {q.get('query')}") 
    print(f"A: {out.get('final_answer')}") 
    print('---')
latency_csv.close()
json.dump(results, open('outputs/logs.json','w'), indent=2)
print('Wrote outputs/logs.json and outputs/latency_report.csv')