import torch
from transformers import pipeline
import time
import os 

#from const import DUMMY_ANS

class Model(): 
    def __init__(self): 
        self.choice = "bruh" 

        if self.choice == "dolly-3b": 
            self.model_name = "databricks/dolly-v2-3b"
        else: 
            self.model_name = "databricks/dolly-v2-3b"

        # TODO make the choice lead to model_name selection 

        print("Creating generator")
        time.sleep(1)
        #self.generator = pipeline(model=self.model_name, torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")
        print("Dummy testing generator created!")

    def generate(self, prompt): 

        os.environ["OPENAI_API_KEY"] = "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"


        print("Waiting for answer w/ ", prompt)

        #res = self.generator(prompt) <-- UNCOMMENT THIS
        #return res[0]["generated_text"]

        time.sleep(1)
        print("Returning answer now!")

        #return DUMMY_ANS

        
