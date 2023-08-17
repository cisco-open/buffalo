import streamlit as st
import requests 
from const import LLM_OPTIONS, BASE_PROMPT, INPUT_SUCCESS, DUMMY_DOCS, SERVER 


def col1(): 

    st.title("Enterprise LLM Gateway")
    model_options = st.multiselect('Select usable Large Language Model(s)', LLM_OPTIONS)
    

    if not st.session_state.demo_state['select_llms']: 
        print(f"(col1) No models currently selected.")
        st.session_state.demo_state['select_llms'] = model_options 


    elif model_options != st.session_state.demo_state['select_llms']: 
        print(f"Change in selection, modifying models now!")
        st.session_state.demo_state['select_llms'] = model_options 

    

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

            with st.spinner('Optimizing...'):
                payload = {'prompt' : text, 'llms' : st.session_state.demo_state['select_llms']}
                response = requests.post(f"{SERVER}/prompt/post", json=payload)
                cost_options = response.json()['cost_options']

                st.session_state.demo_state['cost_options'] = cost_options
                st.session_state.demo_state['cost_options_ready'] = True 



            with st.spinner('Searching cache...'):

                print(f"SEARCHING CACHE WITH [{text}]")
                payload = {'prompt' : text, 'llms' : st.session_state.demo_state['select_llms'], 'add' : False, 'threshold' : 0.8}
                response = requests.post(f"{SERVER}/cache/post", json=payload)

                st.session_state.demo_state['queries'] = response.json()['queries'] 
                st.session_state.demo_state['cache_found'] = response.json()['cache_found'] 
                st.session_state.demo_state['cache_result'] = response.json()['cache_results']  

                st.session_state.demo_state['cache_result_ready'] = True 


            st.success(INPUT_SUCCESS, icon="✅")

          
        elif st.session_state.demo_state['cost_options_ready'] and st.session_state.demo_state['cache_result_ready']: 
            st.success(INPUT_SUCCESS, icon="✅")

    
    st.divider() 

    st.title("Knowledge Base 📁")

    response = requests.get(f"{SERVER}/docs")
    docs_list = response.json()['docs']

    max_filename_length = max(len(filename) for filename, _ in docs_list)

    with st.expander(f"Currently loaded documents ({len(docs_list)}):"):
        for doc, size in docs_list: 
            formatted = f" - {doc:<{max_filename_length}} -- Size: {round(size, 2):>6.2f} kb"
            st.text(formatted)

        st.caption("Pointing to folder /docs/. This relative path be changed in const.py")
