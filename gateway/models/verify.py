
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

import nltk 
import torch 

from openie import StanfordOpenIE

from nltk.tokenize import sent_tokenize 
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from utils.elastic import ElasticVerification

"""

Need to download CoreNLP (???)

"""

class VerificationModel(): 

    def __init__(self, 
                 fact_threshold = 0.9, 
                 fact_model_name = "lighteternal/fact-or-opinion-xlmr-el", 
                 rel_threshold = 0.66, 
                 data_folder_path = None): 
        
        self.FACT_THRESHOLD = fact_threshold
        self.fact_model_name = fact_model_name

        self.fact_tokenizer = AutoTokenizer.from_pretrained(self.fact_model_name)
        self.fact_model = AutoModelForSequenceClassification.from_pretrained(self.fact_model_name)

        self.properties = {
            'openie.affinity_probability_cap': rel_threshold,
        }

        # TODO - Only use docs that come from exfiltrator 
        self.elastic = ElasticVerification(data_folder_path, None)


    @staticmethod
    def split_into_clauses(text):
        def split_sentence_into_clauses(sentence):
            conjunctions = [', and', ', but', ', or', ', so', ', nor', ', yet', ', for', ', because', ', since']
            clauses = []
            temp_clause = []

            words = sentence.split()
            for word in words:
                temp_clause.append(word)
                if word[-1] in [';', ','] or word.lower() in conjunctions:
                    clauses.append(' '.join(temp_clause))
                    temp_clause = []

            if temp_clause:
                clauses.append(' '.join(temp_clause))

            return clauses
        
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        
        # Split sentences into clauses
        all_clauses = []
        for sentence in sentences:
            clauses = split_sentence_into_clauses(sentence)
            all_clauses.extend(clauses)
        
        return all_clauses


    # Input - text (string), output (list of facts)
    def fact_vs_opinion(self, text): 
        # First, split sentence into clauses 

        facts = [] 

        for output in text: 
            print(f"(verify) Looking at: {output}")
            clauses = VerificationModel.split_into_clauses(output)
            num_phrases = len(clauses)

            for clause in clauses: 

                if len(clause.split()) <= 1: 
                    facts.append((clause, None)) 
                    continue 

                inputs = self.fact_tokenizer(clause, return_tensors="pt")

                # Classify the text as fact or opinion
                with torch.no_grad():
                    logits = self.fact_model(**inputs).logits
                    predicted_class = logits.argmax().item()

                # Determine the classification label
                classification_label = "Fact" if predicted_class == 1 else "Opinion"
                print(f"({classification_label}) - {clause}")

                # TODO - Figure out how to get similarity score like they do in HuggingFace 
                facts.append((clause, predicted_class))


        actual_facts = [] 
        annotated_txt = []

        for clause, score in facts: 
            clause = clause.strip() + " "
            if not score or predicted_class== 0: 
                # Means its NOT a fact 
                annotated_txt.append(clause)
            else: 
                annotated_txt.append((clause, "Fact"))
                actual_facts.append(clause)

        return actual_facts, num_phrases, annotated_txt
   

    # Input - list (clauses), output (either None or tuple(e1, rel, e2))
    def get_relations(self, list_of_facts, model): 
     
        relations = [] 
        with StanfordOpenIE(properties=self.properties) as client:
            for fact in list_of_facts: 
                triples = client.annotate(fact)
                if not triples or len(triples) == 0: 
                    relations.append(None)
                    continue 

                temp = []
                for triple in triples:
                    print('|-', triple)
                    temp.append((triple['subject'], triple['relation'], triple['object']))
                    
                relations.append(temp)
              
        return relations 


    # Input - list (triplets) and docs (filepaths), output (tbd)
    def match_triplets(self, list_of_triplets, docs): 
        
        # TODO - Use docs instead of everything inside! 
        list_results = [] 
        if not list_of_triplets: 
            return list_results 
        
        for triplets in list_of_triplets: 
            result = {}
            result['match'] = None 

            if not triplets: 
                list_results.append(result)
                continue 

            for triplet in triplets: 
                print("Currently looking at this triplet", triplet)
                result['sub'], result['rel'], result['obj'] = triplet  
                result['triplet'] = triplet 

                match, score, doc, triplet, context = self.elastic.triplet_match(triplet, docs)

                if match:
                    result['match'] = match 
                    result['score'] = score
                    result['doc'] = doc
                    result['match_triplet'] = triplet
                    result['match_context'] = context
                    break 

                else: 
                    continue 

            if not result['match']: 
                result['match'] = False 
                result['score'] = 0
                result['doc'] = None
                result['match_triplet'] = None
                result['match_context'] = None 

            list_results.append(result)

        return list_results  



if __name__=="__main__": 

    DUMMY_TXT = """The movie released in 1991, and I found that saddening. You see, I really like Beauty and the Beast, because Belle is a Disney princess."""

    vm = VerificationModel() 
    res1, res2 = vm.fact_vs_opinion(DUMMY_TXT)

    print(res1)
    print(res2)

    rels = vm.get_relations(res1, None)
    print(rels)
