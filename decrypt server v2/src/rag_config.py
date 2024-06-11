import numpy as np
from config import Data_loc
from sentence_transformers import SentenceTransformer
from numpy.linalg import norm
import json
import spacy
import faiss
import os

class VectorSearch:
    def __init__(self) -> None:
        self.model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    
    def cosine_similarity(self, x, y):
        return np.dot(x,y)/(norm(x) * norm(y))


class DataPrep:
    def __init__(self) -> None:
        self.filepath = Data_loc
        self.nlp = spacy.load("en_core_web_sm")
        self.temp = []

    def ord_load(self):
        with open(data.filepath, 'r') as file:
            data = json.load(file)
            print(data)
        
    def process_file(self):
        with open(self.filepath, 'r') as file:
            data = json.load(file)
            for item in data:
                url = item['url']
                term = item['term']
                content = item['description']
                docs = self.nlp(content)
                self.temp.extend({'text': doc.text, 'url': url, 'term': term} for doc in docs.sents)

        return self.temp
    
    def data_chunk(self):
        chunks = [chunk for chunk in self.process_file()]

        chunks = [{'id': i, **chunk} for i, chunk in enumerate(chunks)] # use ** to unpack into a new dictionary with id as a new identifier for each dict in the list
        return chunks

class VectorStore(VectorSearch, DataPrep):
    def __init__(self) -> None:
        VectorSearch.__init__(self)
        DataPrep.__init__(self)
        self.sentences = [chunk['text'] for chunk in self.data_chunk()]
        self.faiss_index = None
        self.k = 1 # 2 # 3

    def embed(self, text):
        if isinstance(text, str):
            return self.model.encode([text], show_progress_bar=True)
        else:
            return self.model.encode(text,show_progress_bar=True)

    
    def create_index(self, embeddings):
        embeddings = self.embed(embeddings)
        faiss_index = faiss.IndexFlatIP(self.model.get_sentence_embedding_dimension())
        faiss_index.add(embeddings)

    def retriever(self, query):
        query_embed = self.embed(query)
        # distance, indices, embeddings = self.faiss_index.search_and_reconstruct(query_embed, self.k)
        distance, indices = self.faiss_index.search(query_embed, self.k)

        # context = '\n'.join([f'{i}. {self.sentences[index]}' for i, index in enumerate(indices[0])])
        return distance, indices



if __name__ == '__main__':
    dataprep = DataPrep()
    search = VectorStore()
    # print(dataprep.data_chunk())
    # data.ord_load()
    embeddings = search.embed(search.sentences)
    search.create_index(embeddings)
    query = "what is bitcoin"
    distances, indices = search.retriever(query)
    print(distances, indices)
    # print(VectorStore().sentences)

        
