import torch
import faiss
import os
from transformers import AutoTokenizer, AutoModel
from langchain.document_loaders import DirectoryLoader, TextLoader  # Import TextLoader here

from langchain.document_loaders import TextLoader  
from langchain.indexes import VectorstoreIndexCreator 
from langchain.chat_models import ChatOpenAI


class QACache:
    def __init__(self, 
                 default_model="princeton-nlp/sup-simcse-bert-base-uncased", 
                 embedding=None, 
                 file_path='EnterpriseGateway/docs', 
                 threshold=0.8):
        
        os.environ["OPENAI_API_KEY"] = "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"

        self.default_model = default_model
        self.embedding = embedding

        self.model = AutoModel.from_pretrained(default_model)
        self.tokenizer = AutoTokenizer.from_pretrained(default_model)
       
        self.file_path = file_path
        self.context_index = self.initialize_index()
        self.threshold = threshold 

        self.index = None
        self.questions = []
        self.answers = []



    # def initialize_index(self):
    #     loader = TextLoader(self.file_path)
    #     index = VectorstoreIndexCreator().from_loaders([loader])
    #     return index
    def initialize_index(self, directory='EnterpriseGateway/docs'):
        loader = DirectoryLoader(directory, glob="*.txt")
        index = VectorstoreIndexCreator().from_loaders([loader])
        return index

    def get_huggingface_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)

        sentence_embedding = outputs.last_hidden_state[:, 0]
        return sentence_embedding.numpy()


    def get_embedding(self, input_text):
        input_embedding = self.get_huggingface_embedding(input_text)        
        faiss.normalize_L2(input_embedding)
        return input_embedding


    def get_answer(self, query):
        #return "The answer to my query is FEE FI FO FUM"
        return self.context_index.query(query, llm=ChatOpenAI())


    def find_similar_question_or_add(self, input_question, add=True, threshold=None):
        sim_threshold = self.threshold
        if threshold:
            sim_threshold = threshold
        input_embedding = self.get_embedding(input_question)
        
            
        if self.index is None:
            if add == False:
                return None, None, None
            
            answer = self.get_answer(input_question)

            if "I don't know" not in answer and add == True: 
                self.index = faiss.IndexFlatIP(input_embedding.shape[1])  
                self.index.add(input_embedding)
                self.questions.append(input_question)
                self.answers.append(answer)
            return answer, 0, None
        
        if add == False:
            distances, indices = self.index.search(input_embedding, 1)
            similarity_score = distances[0][0]
            if similarity_score >= sim_threshold:
                return self.answers[indices[0][0]], similarity_score, indices[0][0]
            else:
                return None, None, None
            
        distances, indices = self.index.search(input_embedding, 1)
        similarity_score = distances[0][0]
        
        if similarity_score >= sim_threshold:
            return self.answers[indices[0][0]], similarity_score, indices[0][0]
        else:
            answer = self.get_answer(input_question)
            if "I don't know" not in answer and add == True:
                self.index.add(input_embedding)
                self.questions.append(input_question)
                self.answers.append(answer)
            return answer, similarity_score, indices[0][0]
   

    # The main cache search function --> exposed in REST API 

    def search(self, query, add=True, threshold=None):
        sim_threshold = self.threshold
        if threshold:
            sim_threshold = threshold

        response, similarity_score, answer_index = self.find_similar_question_or_add(query, add=add, threshold=threshold)

        if response is None:
            return False, None, None
        
        if similarity_score > sim_threshold:
            return True, self.questions[answer_index], response
       
        return False, None, response


