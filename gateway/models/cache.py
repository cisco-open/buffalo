
# Copyright 2022 Cisco Systems, Inc. and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

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
                 data_folder_path=None, 
                 embedding=None, 
                 threshold=0.8, 
                 api_keys=None):
        
        os.environ["OPENAI_API_KEY"] = api_keys["gpt-3.5"]

        self.default_model = default_model
        self.embedding = embedding

        self.model = AutoModel.from_pretrained(default_model)
        self.tokenizer = AutoTokenizer.from_pretrained(default_model)
       
        loader = DirectoryLoader(data_folder_path, glob="*.txt")
        self.context_index = VectorstoreIndexCreator().from_loaders([loader])
        
        self.threshold = threshold 

        self.index = None
        self.questions = []
        self.answers = []


    def get_embedding(self, input_text):
        inputs = self.tokenizer(input_text, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)

        input_embedding = outputs.last_hidden_state[:, 0].numpy()  
        faiss.normalize_L2(input_embedding)
        return input_embedding


    def get_answer(self, query):
        return self.context_index.query(query, llm=ChatOpenAI())


    # Returns: response, sim_score, ans_index 
    def find_similar_question(self, input_question, threshold=None): 
        sim_threshold = self.threshold
        if threshold: sim_threshold = threshold

        input_embedding = self.get_embedding(input_question)

        if not self.index: 
            return None, None, None 
        
        distances, indices = self.index.search(input_embedding, 1)
        similarity_score = distances[0][0]

        if similarity_score >= sim_threshold:
            return self.answers[indices[0][0]], similarity_score, indices[0][0]
        
        return None, None, None 


    def add_to_cache(self, input_question, response):
        input_embedding = self.get_embedding(input_question)

        if not self.index: 
            self.index = faiss.IndexFlatIP(input_embedding.shape[1])  
        
        self.index.add(input_embedding)
        self.questions.append(input_question)
        self.answers.append(response)
   

    # The main cache search function --> exposed in REST API 
    # Returns found (bool), similar_q (str), answer (str)

    def search(self, query, threshold=None):
        sim_threshold = self.threshold
        if threshold: sim_threshold = threshold

        response, similarity_score, answer_index = self.find_similar_question(query, threshold=sim_threshold)
        
        if not response: return False, None, None 
        return bool(response), self.questions[answer_index], response
       

