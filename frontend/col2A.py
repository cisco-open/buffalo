
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

import requests 
import streamlit as st

from const import *



def col2A(): 

    with st.expander(EXPANDER_TEXT, expanded=(not st.session_state.demo_state['selected_generation'])):
        st.title("Prompt Distillation, Normalization, Optimization.")

        # 01) Display Cost Options to User 
        options = st.session_state.demo_state['cost_options']

        if options: 
            st.subheader(f"The prompt has been split into {len(options[0]['combo'])} options. Please select an option:")

            for idx, elem in enumerate(options[0]['combo']): 
                query, _ = elem 
                st.markdown(f"{idx+1}. {query}")

            parsed_options, option_dict = parse(options)
            prompt_choice = st.radio('Cost Options:', parsed_options, label_visibility='collapsed')

            if prompt_choice: 
                st.info(f"Currently Selected: {prompt_choice}")
                st.session_state.demo_state['prompt_choice'] = prompt_choice
                st.session_state.demo_state['query_dict'] = option_dict[prompt_choice]



            # 02) Display Cache Results to User 
            st.subheader("Cache Results:")

            if not st.session_state.demo_state['cache_found']: 
                st.error("Alert! No cache results found.", icon="🚨")
            else: 
                answers = st.session_state.demo_state['cache_result']
                for ans in answers:
                    if ans: 
                        st.success(f"(Cache) -- {ans}", icon="✅")


            # 03) If User Selects "Proceed to LLM(s)"
            # TODO - If cache partial hit, need option to ONLY query LLM w/ non-cache hit (some way to specify for each)
            
            st.divider() 

            if st.button(f'Proceed Using Selected Option'):
                st.session_state.demo_state['selected_generation'] = True 


                output_responses = [] 
                for idx, prompt in enumerate(st.session_state.demo_state['query_dict']): 
                    llm = st.session_state.demo_state['query_dict'][prompt]
                    print(f"(col2A) Using {llm}, searching for: {prompt}")

                    payload = {'prompt' : prompt, 'llm' : llm}
                    response = requests.post(f"{SERVER}/cache/model/post", json=payload)
                    llm_output = response.json()['doc_specific_res']
                    print(f"(col2A) - Cache-LLM: {llm_output}")

                    if not llm_output:  
                        payload = {'prompt' : prompt, 'llm' : llm}
                        response = requests.post(f"{SERVER}/model", json=payload)
                        llm_output = response.json()['general_res']
                        print(f"(col2A) - Genr-LLM: {llm_output}")
                    
                    output_responses.append(llm_output)

                    
                st.session_state.demo_state['output_response_list'] = output_responses


                # For each LLM response, need to run exfiltration check BEFORE displaying ANYTHING to the user. 
                # TODO - Separate this so each LLM query is run/checked independently 
                
                payload = {'text_list' : st.session_state.demo_state['output_response_list']}
                response = requests.post(f"{SERVER}/exfiltrator/post", json=payload)
                st.session_state.demo_state['output_list_exfiltrated'] = response.json()['output_list_exfiltrated'] # TODO - this should be a list of either output or <DOC_EXFIL> flags 
                st.session_state.demo_state['leak_list'] = response.json()['leak_list'] # TODO - this should be a list of lists [[doc1, co2, doc3], [], [doc2], ..]
                st.session_state.demo_state['any_leak'] = response.json()['any_leak'] # TODO - whether ANY leak was found  


                # TODO - do this AFTER the verification score is computed
                # Add relevant things back to cache 
                print(st.session_state.demo_state['output_list_exfiltrated'])
                for idx, output in enumerate(st.session_state.demo_state['output_list_exfiltrated']): 
                    if "<DOC_EXFIL_FLAG" not in output: 
                        payload = {'prompt' :  st.session_state.demo_state['input_list_redacted'][idx], 'output' : output}
                        response = requests.post(f"{SERVER}/cache/add/post", json=payload)

        else: 
            st.error("Please select 'Submit to Prompt & Cost Optimization Layer' to view model options.", icon="🚨")



"""

Helper Functions (NOT STREAMLIT)

"""

def parse(combos):
    if not combos: return [] 

    options = []
    options_dict = {} 

    for elem in combos:

        choice_dict = {} 
        option = f"(Cost: ${round(elem['cost'], 5)}) -- "
        for part, model in elem['combo']: 
            option += f"{model}('{part}') + "
            choice_dict[part] = model 
        options.append(option[:-2])

        options_dict[option[:-2]] = choice_dict 
        
    return options, options_dict
