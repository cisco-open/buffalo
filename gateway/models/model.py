
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


        
