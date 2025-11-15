import pandas as pd
from pydantic import BaseModel, Field, ValidationError

class CSVLookupParams(BaseModel):
    item: str = Field(..., description='Item name to lookup')

class Actor:
    def __init__(self, csv_path='data/prices.csv'):
        self.csv_path = csv_path
        self.df = pd.read_csv(self.csv_path)

    def csv_lookup(self, params: dict):
        try:
            p = CSVLookupParams(**params)
        except ValidationError as e:
            return {'error':'invalid_params', 'detail': e.errors()}
        row = self.df[self.df['item'].str.lower()==p.item.lower()]
        if row.empty:
            return {'found':False, 'item': p.item}
        return {'found':True, 'item': row.iloc[0].to_dict()}