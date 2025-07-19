from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch

class RecipeMatcher:
    def __init__(self, df):
        self.df = df
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.embeddings = self.model.encode(df['search_text'].tolist(), convert_to_tensor=True, show_progress_bar=True)
    
    def find_matching_recipes(self, query, top_k=3):
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        
        cos_scores = util.cos_sim(query_embedding, self.embeddings)[0]

        top_results = torch.topk(cos_scores, k=top_k).indices

        return self.df.iloc[top_results].to_dict('records')