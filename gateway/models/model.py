import torch
from transformers import pipeline
import time
import os 
import openai 

#from const import DUMMY_ANS

class Model(): 
 
    def __init__(self, list_of_models, api_keys): 

        # TODO: currently not using list_of_models, initializing everything instead 
        model_objs = {} 

        self.dolly3b = pipeline(model="databricks/dolly-v2-3b", torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")
        openai.api_key = api_keys['gpt-3.5']

 
    def generate(self, llm, text): 

        # TODO: Would be nice to add panoptica functionality! (or maybe in prompt layer for better separation!)

        print(f"(model) Using {llm}, querying w/: {text}")

        res = "<NO VALID LLM>"

        if llm == "gpt-3.5": 
            # TODO : add 'role' : 'system" to inject prompt additions here! 
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{'role' : 'user', 'content' : text}],
            )
            res = res['choices'][0]['message']['content']

        elif llm == "dolly-3b":
            res = self.dolly3b(text)[0]["generated_text"] 


        return res 


        
