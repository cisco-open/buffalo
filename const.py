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

These are streamlit-specific constants, used by the main.py and frontend/*. 

All BUFFALO related constants can be found in the gateway/ folder. 

"""

# Used for st.session_state

INITIAL_STATE =  {
        # Base I/O in Col1 
        'select_llms' : None, # List of which LLMs have been selected 
        'input_prompt' : None, # Raw text of user input (what is entered in box)

        # Prompt Layer States 
        'input_list' : [], # Split queries after Prompt Layer runs 
        'input_list_redacted' : [], # Split queries after Prompt w/ Redactions
        'cost_options' : None, # Cost Options from Prompt Layer 
        'cost_options_ready' : False, # Whether Cost Options have been computed 

        # Cache Layer States 
        'cache_result' : [], # List of cache results (same dim as input_prompt_list)
        'cache_found' : False, # Whether ANY query returned a hit 
        'cache_result_ready' : False, 


        # Base I/O in Col2A 
        'prompt_choice' : None, # The raw radio item of what is selected 
        'query_dict' : None, # A dictionary of {'prompt_str' : 'model_str'}
        'selected_generation' : False, # Whether we have clicked "Query LLM"
        'output_response_list' : [], # Raw LLM generated-output for each subprompt (list)

        # Leak Layer States 
        'output_list_exfiltrated' : [], # A list of either output or <DOC_EXFIL> flags 
        'leak_list' : [], # A list of lists [[doc1, co2, doc3], [], [doc2], ..]
        'any_leak' : False, # Whether ANy leak was found 


        # Base I/O in Col2B 
        'input_topic_list' : [], # List of (doc, score) tuples 
        'output_topic_list' : [], # List of (doc, score) tuples 
        'triplet_doc_list' : [], # List of file names to check against
        
        # Verify Layer States
        'list_of_facts' : [], # List of facts given all of output_list 
        'list_of_relations' : [], # For each extracted fact, list of relation tuples 

        # docs_found_in is a dictionary of freq_counts, such that {'doc_name' : 'num_facts_found_in_this_doc'}
        'verify_metrics' : {'num_phrases' : 0, 'num_facts' : 0, 'num_triplets' : 0, 'num_matched' : 0, 'docs_found_in' : {}}
    }


# Constant texts used for st components 

EXPANDER_TEXT = "Cost, Prompt, and Cache options will be shown in this expander. Please select an option by using the 'Proceed' button below. Feel free to hide me when you're finished."

BASE_PROMPT = ""

RADIO_ITEMS = "The default option has been preselected. Combinations and options are shown below."

INPUT_SUCCESS = "Results of Prompt and Cache Layer are discussed to the right!"

SERVER = "http://enterprisellmbackend:3000"

SENSITIVITY_SLIDER_TEXT = "Sensitivity of Document Embeddings (top-k, 1 = strict, 4 = flexible). Default selection is 2, meaning top-2 documents are chosen for both prompt and response 🔎."

TAB_TITLES = ["Base I/O", "Doc Identification", "Fact vs. Opinion", "Relation Extraction", "Triplet Matching", "Final Statistics"]
