
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

import streamlit as st
import requests 
from const import BASE_PROMPT, INPUT_SUCCESS, SERVER 


def col1(): 

    st.title("Enterprise LLM Gateway")


    # 01) Model Selection 

    response = requests.get(f"{SERVER}/model_list")
    model_list = response.json()['model_list']

    model_options = st.multiselect('Select usable Large Language Model(s)', model_list)
    
    if not st.session_state.demo_state['select_llms']: 
        print(f"(col1) No models currently selected.")
        st.session_state.demo_state['select_llms'] = model_options 

    elif model_options != st.session_state.demo_state['select_llms']: 
        print(f"(col1) Change in selection, modifying models now!")
        st.session_state.demo_state['select_llms'] = model_options 

    
    # 02) Entering Prompt 

    with st.form("my_form"):
        text = st.text_area("Enter Prompt:", BASE_PROMPT)
        submitted = st.form_submit_button(f"Submit to Prompt & Cost Optimization Layer")\
        
        if len(st.session_state.demo_state['select_llms']) == 0:
            st.info("Please select at least LLM to continue")
        
        elif len(text) == 0: 
            st.info("Please enter at least one word to continue")

        elif submitted:
            st.session_state.demo_state['input_prompt'] = text
            st.session_state.demo_state['selected_generation'] = False  

            # 02A) Pass prompt/llms through Prompt Layer 

            with st.spinner('Optimizing...'):
                payload = {'prompt' : text, 'llms' : st.session_state.demo_state['select_llms']}
                response = requests.post(f"{SERVER}/prompt/post", json=payload)
                print(f"(col1) Received cost options from Prompt Layer.")

                st.session_state.demo_state['input_list_redacted'] = response.json()['input_list_redacted']
                st.session_state.demo_state['input_list'] = response.json()['input_list']
                st.session_state.demo_state['cost_options'] = response.json()['cost_options']
                st.session_state.demo_state['cost_options_ready'] = True 

                print(f"(col1) Input List Redacted: {st.session_state.demo_state['input_list_redacted']}")
                print(f"(col1) Cost Options: {st.session_state.demo_state['cost_options']}")



            # 02B) Pass prompt/llms through Cache Layer 

            with st.spinner('Searching cache...'):

                print(f"(col1) Searching cache w/ {len(st.session_state.demo_state['input_list'])} queries.")

                # TODO - removed threshold, changed prompt to prompt_list 
                payload = {'prompt_list' : st.session_state.demo_state['input_list']} 
                response = requests.post(f"{SERVER}/cache/search/post", json=payload) 

                st.session_state.demo_state['cache_found'] = response.json()['cache_found'] 
                st.session_state.demo_state['cache_result'] = response.json()['cache_results'] 
                st.session_state.demo_state['cache_result_ready'] = True 


            st.success(INPUT_SUCCESS, icon="✅")

          
        elif st.session_state.demo_state['cost_options_ready'] and st.session_state.demo_state['cache_result_ready']: 
            st.success(INPUT_SUCCESS, icon="✅")

    
    st.divider() 


    # 03) Displaying Knowledge Base (if toggled on, default True)

    response = requests.get(f"{SERVER}/docs")
    docs_list = response.json()['docs']
    docs_path = response.json()['path']
    docs_show = response.json()['show']

    st.title("Knowledge Base 📁")

    if not docs_show: 
        st.info(f"Displaying of KB is off. This can be toggled in gateway/admin.yml")
    
    else: 
        max_filename_length = max(len(filename) for filename, _ in docs_list)

        with st.expander(f"Currently loaded documents ({len(docs_list)}):"):
            for doc, size in docs_list: 
                formatted = f" - {doc:<{max_filename_length}} -- Size: {round(size, 2):>6.2f} kb"
                st.text(formatted)

            st.caption(f"Pointing to folder {docs_path}. This relative path be changed in gateway/admin.yml")
