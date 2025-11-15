from fastapi import FastAPI
from src.actor import Actor
app = FastAPI()
actor = Actor()

@app.get('/health')
def health():
    return {'status':'ok'}

@app.get('/lookup/{item}')
def lookup(item: str):
    return actor.csv_lookup({'item': item})