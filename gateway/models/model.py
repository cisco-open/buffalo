import torch
from transformers import pipeline
import time
import os 
import openai 

#from const import DUMMY_ANS

class Model(): 
 
    def __init__(self): 
        self.dolly3b = pipeline(model="databricks/dolly-v2-3b", torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")

        self.api_key = "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"
        openai.api_key = self.api_key

 
    def generate(self, llm, text): 
        print(f"(model) Using {llm}, querying w/: {text}")

        res = "<NO VALID LLM>"

        if llm == "gpt-3.5": 
            res = openai.Completion.create(
                engine="text-davinci-003",  
                prompt=text,
                max_tokens=100  # Adjust as needed
            )


        elif llm == "dolly-3b":
            res = self.dolly3b(text)[0]["generated_text"] 


        return res 


        
