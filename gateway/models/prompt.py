
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

import re
import itertools 
from nltk.tokenize import sent_tokenize


class QueryProcessor:
    def __init__(self):
        self.MODEL_COSTS = {
            "gpt-3.5": 0.06 / 1000,  # $0.06 per 1000 tokens
            "dolly-3b": 0.01 / 1000,  # $0.06 per 1000 tokens
            "gpt-4": 0.08 / 1000,  # $0.08 per 1000 tokens
        }

        # List of regex patterns and their corresponding modifications
        self.PATTERNS = [
                # Coding tasks
                (r"write a function that", "imagine you are a Python expert and you had to write a function that"),
                (r"create a program that", "imagine you are an experienced programmer and you need to create a program that"),
                
                # Teaching or explaining
                (r"explain how", "imagine you are teaching someone and you need to explain how"),
                (r"describe the process of", "imagine you are an instructor and you need to describe the process of"),
                
                # Problem-solving
                (r"solve the problem of", "imagine you are solving the problem of"),
                (r"find a solution for", "imagine you are tasked with finding a solution for"),

                # Writing
                (r"write a story about", "imagine you are a storyteller and you need to write a story about"),
                (r"compose a poem on", "imagine you are a poet and you need to compose a poem on"),

                # Scientific explanation
                (r"explain the concept of", "imagine you are a scientist and you need to explain the concept of"),

                # Opinion or debate
                (r"what are your thoughts on", "imagine you are in a debate and you need to share your thoughts on"),

                # Personal narrative
                (r"tell me about a time when", "imagine you are sharing a personal experience when"),

                # General instructions
                (r"provide instructions for", "imagine you are giving clear instructions for"),

                # Math problems
                (r"solve for x in", "imagine you are solving for x in"),

                # History-related
                (r"describe the historical event of", "imagine you are describing the historical event of"),

                # Geography and travel
                (r"plan a trip to", "imagine you are planning a trip to"),

                # Technology and gadgets
                (r"explain how a", "imagine you are explaining how a"),

                # Cooking and recipes
                (r"create a recipe for", "imagine you are creating a recipe for"),

                # Health and fitness
                (r"design a workout routine for", "imagine you are designing a workout routine for"),

                # Art and design
                (r"sketch a drawing of", "imagine you are sketching a drawing of"),

                # Career and job-related
                (r"prepare for a job interview as", "imagine you are preparing for a job interview as"),

                # Custom patterns
                # (r"your_pattern_here", "imagine you are customizing the prompt here"),

                # Add more patterns as needed
            ]


    def modify_input_for_prompt(self, input_list):
        injected_inputs = [] 
        for subprompt in input_list: 
            print(f"(prompt) Analyzing subprompt: {subprompt}")
            for pattern, replacement in self.PATTERNS:
                if re.search(pattern, subprompt, re.IGNORECASE):
                    input_string = re.sub(pattern, replacement, subprompt, flags=re.IGNORECASE)
                    subprompt = input_string 
                    print(f"(prompt) - Injected: {replacement}")
                    break  

            injected_inputs.append(subprompt)

        return injected_inputs 
    

    # TODO - can use external library (ex microsoft presidio)
    # TODO - add in context-aware research 

    @staticmethod
    def redact_phone(s):
        phone_pattern = r'\b(\+\d{1,3}[-.]?)?(\()?(\d{3})(?(2)\))[-. ]?\d{3}[-.]?\d{4}\b'
        if re.search(phone_pattern, s):
            s = re.sub(phone_pattern, '**(Redacted Phone Num)**', s)
            return True, s
        else:
            return False, s
        
    @staticmethod
    def redact_ssn(s):
        ssn_pattern = r'\b\d{3}-?\d{2}-?\d{4}\b'
        if re.search(ssn_pattern, s):
            s = re.sub(ssn_pattern, '**(Redacted SSN)**', s)
            return True, s
        else:
            return False, s
        
    @staticmethod
    def redact_email(s):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.search(email_pattern, s):
            s = re.sub(email_pattern, '**(Redacted Email)**', s)
            return True, s
        else:
            return False, s

    @staticmethod
    def decompose_query(query):
        return sent_tokenize(query)


    def calculate_cost(self, text, model):
        tokens = len(text)
        return round(tokens * self.MODEL_COSTS[model], 5)


    def redact_query_list(self, input_list): 
        redacted_list = []
        for text in input_list: 
            print(f"(prompt) Redacting: {text}")
            _, text = self.redact_phone(text)
            _, text = self.redact_ssn(text)
            _, text = self.redact_email(text)
            redacted_list.append(text)
        
        return redacted_list 


    def get_combination_options(self, query_list, model_list):
        combinations = []
        print(f"(prompt) query_list: {query_list}, model_list: {model_list}")

        for query_permutation in list(itertools.product(model_list, repeat=len(query_list))):
            print(query_permutation)
            combination = list(zip(query_list, query_permutation))
            
            cost = sum(self.calculate_cost(query, model) for query, model in combination)
            combinations.append({'combo' : combination, 'cost' : cost})
    
        print(f"(prompt) Total of {len(combinations)} unfiltered combos.")
        combinations.sort(key=lambda x: x["cost"])
        combinations = self.filter_results(combinations, 4) # TODO - make this 4 come from admin.yml 

        return combinations
    

    #User specifies how many options they want to see. If n is 1 they will see the cheapest option, if n is 2 they will see the cheapest and most expensive poption, if n > 2 they will see the cheapest, most expensive, and n - 2 next cheapest
    def filter_results(self, costs, n):
        if n >= len(costs):
            return costs
        if n < 1:
            return []
        elif n == 1:
            return costs[0]
        elif n == 2:
            return costs[0] + costs[len(costs) - 1]
        else:
            return costs[0:n-1] + [costs[len(costs) - 1]]


# tst = QueryProcessor()
# print(tst.get_combination_options(["Query1", "Q1", "Q2", "Q4"], ["gpt-3.5"]))
