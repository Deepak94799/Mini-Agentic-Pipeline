import os, time, json, re
from src.retriever import Retriever
from src.reasoner import Reasoner
from src.actor import Actor

class Planner:
    def __init__(self, docs_path='docs'):
        self.retriever = Retriever(docs_path=docs_path)
        self.reasoner = Reasoner()
        self.actor = Actor()

    def _extract_item(self, query):
        # Try quoted item first
        match = re.search(r"'([^']+)'|\"([^\"]+)\"", query)
        if match:
            return (match.group(1) or match.group(2)).strip()
        # fallback: remove punctuation and take last two words
        words = re.sub(r'[?.]', '', query).split()
        if len(words) >= 2:
            return ' '.join(words[-2:]).strip()
        return words[-1].strip()

    def handle(self, query):
        trace = {'query': query, 'steps': [], 'timings': {}}
        t0 = time.time()

        # Retrieval
        r = self.retriever.retrieve(query)
        trace['steps'].append({'step': 'retrieval', 'output': r})
        trace['timings']['retrieval'] = r.get('elapsed', None)
        context = '\n'.join([h.get('text','') for h in r.get('hits', [])])

        # Reasoner decision
        t1 = time.time()
        d = self.reasoner.decide(query, context)
        trace['steps'].append({'step': 'reasoner', 'output': d})
        trace['timings']['reasoner'] = d.get('elapsed', None)

        final_answer = None
        use_tool = False
        item = None

        # Determine decision source
        if d.get('decision') == 'tool':
            use_tool = True
        elif d.get('decision') == 'llm' and d.get('llm_json'):
            dec = d['llm_json'].get('decision', {})
            use_tool = bool(dec.get('use_tool'))
            if use_tool:
                tc = dec.get('tool_call', {})
                item = tc.get('params', {}).get('item')

        # If decided to use tool, ensure item is extracted
        if use_tool:
            if not item:
                item = self._extract_item(query)
            t_tool = time.time()
            tool_res = self.actor.csv_lookup({'item': item})
            trace['steps'].append({'step': 'actor_call', 'output': tool_res})
            trace['timings']['actor'] = time.time() - t_tool
            if tool_res.get('found'):
                it = tool_res['item']
                final_answer = f"{it.get('item')}: price INR {it.get('price_inr')}, stock {it.get('stock')} (source_date: {it.get('source_date')})"
            else:
                final_answer = f"No data for {item}. Context: {context[:200]}"
        else:
            # KB or LLM answer, with fallback heuristic for numeric queries
            if d.get('decision') == 'kb':
                kb_answer = d.get('answer', '') or ''
                final_answer = kb_answer

                lowered = query.lower()
                numeric_keywords = ['price', 'stock', 'in stock', 'how much', 'source_date', 'lookup price', 'lookup stock']
                wants_numeric = any(lowered.strip().startswith(k) or k in lowered for k in numeric_keywords)
                has_digits = any(ch.isdigit() for ch in kb_answer)

                if wants_numeric and not has_digits:
                    # fallback to tool
                    fallback_item = self._extract_item(query)
                    t_tool = time.time()
                    tool_res = self.actor.csv_lookup({'item': fallback_item})
                    trace['steps'].append({'step':'actor_call_fallback','output':tool_res})
                    trace['timings']['actor_fallback'] = time.time() - t_tool
                    if tool_res.get('found'):
                        it = tool_res['item']
                        final_answer = f"{it.get('item')}: price INR {it.get('price_inr')}, stock {it.get('stock')} (source_date: {it.get('source_date')})"
            elif d.get('decision') == 'llm':
                final_answer = d.get('llm_text')
            else:
                final_answer = 'Unable to decide.'

        trace['final_answer'] = final_answer
        trace['timings']['total'] = time.time() - t0
        return trace
