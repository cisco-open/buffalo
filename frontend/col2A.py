import requests 
import streamlit as st

from const import *



def col2A(): 

    with st.expander(EXPANDER_TEXT, expanded=(not st.session_state.demo_state['selected_generation'])):
        st.title("Prompt Distillation, Normalization, Optimization.")

        options = st.session_state.demo_state['cost_options']

        if options: 
            st.subheader(f"The prompt has been split into {len(options[0]['combo'])} options. Please select an option:")

            for idx, elem in enumerate(options[0]['combo']): 
                _, part = elem 
                st.markdown(f"{idx+1}. {part}")

            prompt_choice = st.radio('', parse(options))

            if prompt_choice: 
                st.info(f"Currently Selected: {prompt_choice}")



            st.subheader("Cache Results:")

            if not st.session_state.demo_state['cache_found']: 
                st.error("Alert! No cache results found.", icon="🚨")
            else: 
                answers = st.session_state.demo_state['cache_result']
                for ans in answers:
                    if ans: 
                        st.success(f"(Cache) -- {ans}", icon="✅")


            st.divider() 

            if st.button(f'Proceed Using Selected Option'):

                # TODO - change this so LLM output is separate from cache!! 

                if "Panoptica:" == st.session_state.demo_state['input_prompt'].split()[0]: 
                    # Call PanopticaGPT functions 
                    pass 
                
                print("CALLING LLM W?", st.session_state.demo_state['input_prompt'])
                payload = {'prompt' : st.session_state.demo_state['input_prompt'], 'llms' : st.session_state.demo_state['select_llms'], 'add' : True, 'threshold' : 2}
                response = requests.post(f"{SERVER}/cache/post", json=payload)
                llm_output = response.json()['cache_results']

                # How many employees are there? What did you think of the Brother Grimm's Rapunzel??"
                #llm_output = ["<DOC_EXFIL_FLAG>", 
                #              """I think that the Brother Grimm's Rapunzel is a great short story. Rapunzel has long hair and is magical. A witch raises Rapunzel and keeps her secluded until a prince finds and climbs into the tower.  He approaches her with her long hair, but the witch eventually discovers their interactions.  Rapunzel is banished, and the prince is blinded. After trials, Rapunzel's tears heal his eyes, and they reunite for a happy ending."""]

                st.session_state.demo_state['selected_generation'] = True 
                st.session_state.demo_state['output_response'] = " ".join(llm_output)
                st.session_state.demo_state['output_response_list'] = llm_output

                #st.session_state.demo_state["output_response"] = """I think that the Brothers Grimm's Rapunzel is a timeless tale of a girl locked in a tower by a witch. The witch raises Rapunzel and keeps her secluded until a prince hears her singing. He visits her with her long hair, but the witch eventually discovers their secret meetings. Rapunzel is banished, and the prince is blinded. After trials, Rapunzel's tears heal his eyes, and they reunite for a happy ending, showcasing resilience and the power of love in the face of challenges."""

        else: 
            st.error("Please select 'Submit to Prompt & Cost Optimization Layer' to view model options.", icon="🚨")




def parse(combos):
    if not combos: return [] 

    options = []
    for elem in combos:
        option = f"(Cost: ${round(elem['cost'], 5)}) -- "
        for model, part in elem['combo']: 
            option += f"{model}('{part}') + "
        options.append(option[:-2])
        
    return options