
# Copyright 2024 Cisco Systems, Inc. and its affiliates
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

"""

The following was original use.py -- need to add for topic extraction!!! 

"""


import os
import glob
import tensorflow as tf
import tensorflow_hub as hub

def load_documents_from_folder(folder_path):
    documents = []
    file_paths = glob.glob(os.path.join(folder_path, '*.txt'))
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            document_text = file.read().strip()
            documents.append(document_text)
    return documents

def calculate_similarity_scores(input_text, document_set):
    module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/5"
    model = hub.load(module_url)

    print("Loaded in the model")

    # Encode the input text and documents
    input_embedding = model([input_text])
    document_embeddings = model(document_set)

    print("Got the embeddings")

    # Calculate cosine similarity between the input text and each document
    similarity_scores = tf.keras.losses.cosine_similarity(input_embedding, document_embeddings)
    return similarity_scores

if __name__ == "__main__":
    BASE_PROMPT = "What lesson did Hansel and Gretel teach to children, and how is this similar to the lesson taught by the princess locked in the tower"
    DUMMY_ANS = """Hansel and Gretel teaches children the value of family bonds, as the siblings support and protect each other throughout their journey. The tale warns against trusting strangers blindly, as the wicked witch lures the children with her candy-coated house, revealing the dangers of deceitful individuals. The children's use of breadcrumbs as a trail reflects the importance of planning and foresight in difficult situations, showing the significance of being prepared. Similarly, the princess locked in the tower, like Rapunzel, showcases resilience and patience while using her long hair as a resource to aid her escape, emphasizing the power of adaptability and ingenuity."""

    input_text = DUMMY_ANS
    folder_path = "../docs/"  # Replace with the folder containing text files

    print("Boutta load docs")

    document_set = load_documents_from_folder(folder_path)

    print("Boutta compute scores")

    similarity_scores = calculate_similarity_scores(input_text, document_set)

    # Print similarity scores
    for i, score in enumerate(similarity_scores):
        print(f"Document {i+1}: Similarity Score: {score.numpy():.4f}")




"""

The following was copied from older version of verify.py

"""

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
nlp = pipeline("ner", model=model, tokenizer=tokenizer)

text = "To address this, the Nixon Administration began multilateral negotiations with the combatants. They arranged for Israel to pull back from the Sinai Peninsula and the Golan Heights."

def extract_keywords(text): 
    entities = nlp(text)

    consolidated_entities = []
    current_entity = None

    for entity in entities:
        if current_entity is None:
            current_entity = entity
        elif entity['start'] <= current_entity['end'] + 1:
            current_entity['word'] += ' ' + entity['word']
            current_entity['end'] = entity['end']
        else:
            consolidated_entities.append(current_entity)
            current_entity = entity

    if current_entity is not None:
        consolidated_entities.append(current_entity)
    
    print(f"Consolidated_Entities: {consolidated_entities} \n")

    # Now, need to format this! 

    return format_keywords(text, consolidated_entities), consolidated_entities


def format_keywords(text, entities): 
    res = []
    
    subsets = [] 
    prev_index = 0

    keys = {}

    for entity in entities: 
        keys[entity['start']] = [entity['word'], entity['entity']]

        subsets.append((prev_index, entity['start']))
        prev_index = entity['start']
        subsets.append((prev_index, entity['end']))
        prev_index = entity['end']

    subsets.append((prev_index, len(text)))
    print(subsets)

    for s, e in subsets: 
        if s in keys: 
            res.append((keys[s][0], keys[s][1]))
        else: 
            res.append(text[s:e])

    print(res)
    return res 


def get_topic_info(entities): 
    res = [] 
    for entity in entities: 
        pass 
        
        
    return res 

#print(extract_keywords(text))
