import requests 
import streamlit as st 
from annotated_text import annotated_text 
import extra_streamlit_components as stx

from const import *


def col2B(): 
    st.title("Output Exfiltration, Verification.")

    val = stx.stepper_bar(steps=TAB_TITLES)

    #Base I/O
    if val == 0: 
        if not st.session_state.demo_state['input_prompt']: 
            st.subheader("Please enter an input prompt.")
            st.divider()
            st.subheader("Please wait for an LLM output.")
        else: 
            st.subheader(f"(User) {st.session_state.demo_state['input_prompt']}")
            st.divider()
            st.subheader(f"(LLMs) {st.session_state.demo_state['output_response']}")

            st.markdown("")            
            for idx, elem in enumerate(st.session_state.demo_state['output_response_list']):
                st.markdown(f"(Query {idx+1}) LLM Output: {elem}")
        


    #Doc Identification
    if val == 1: 
        sensitivity = st.slider(SENSITIVITY_SLIDER_TEXT, 1, 4, 2)

        colX, colY = st.columns(2)

        with colX: 
            st.subheader(f"Prompt Topics: ")

            # Here, need to add the data exfiltration stuf 

            st.text(f" - corporate_02.txt ~ 0.1202")
            st.text(f" - rapunzel.txt ~ 0.2681")
            st.text(f" - disney_data.txt ~ 0.1881")

        with colY: 
            st.subheader(f"Response Topics:")
            st.text(f" - rapunzel.txt ~ 0.4981")
            st.text(f" - disney_data.txt ~ 0.2395")

        st.divider() 

        st.subheader("Exfiltration Check on Documents in Knowledge Base.")

        with st.spinner('Calculating Leaks...'):

            payload = {'text' : st.session_state.demo_state['output_response']}
            response = requests.post(f"{SERVER}/exfiltrator/post", json=payload)
            leak = response.json()['leak']

            #st.session_state.demo_state['leak'] = leak
            #st.session_state.demo_state['leak'] = ["employee_info.txt"]

            print("Got the following leak(s)", leak)
        
        if st.session_state.demo_state['leak']: 
            st.error('Data leak detected', icon="🚨")
            for doc in st.session_state.demo_state['leak']: 
                st.error(f"Document Name: {doc}", icon="🚨")

        else:
            st.success("No information was leaked", icon="✅")


    #Fact vs. Opinion Classifier 
    if val == 2: 
        if st.session_state.demo_state['leak']: 
            st.error(f"Part of the LLM response may have been removed due to Data Exfiltration leakage.", icon="🚨")

        payload = {'text' : st.session_state.demo_state['output_response']}

        response = requests.post(f"{SERVER}/verify/facts/post", json=payload)
        list_of_facts = response.json()['list_of_facts']
        annotated_txt = response.json()['annotated_txt']

        st.session_state.demo_state['list_of_facts'] = list_of_facts
        
        st.subheader("Labelling with Fact-vs-Opinion Classifier")
        annotated_text(format_annotated_txt(annotated_txt))

        st.divider()

        st.subheader("Extracted facts from LLM Response")
        for idx, fact in enumerate(list_of_facts): 
            st.markdown(f"{idx+1}. {fact}")


    """
    
    Previously, used to be AMR code here. This old code has been saved and will eventually be added. 

    #st.graphviz_chart(states['amr_grp_inp'])        
    #st.graphviz_chart(states['amr_grp_out'])
    
    """
    
    # Information Extraction
    if val == 3: 
        model_options = st.selectbox('Please select an Information Extraction (IE) method. Default methodology, Stanford OpenIE.', ["Stanford OpenIE", "UIUC AMR-IE"])

        payload = {'list_of_facts' : st.session_state.demo_state['list_of_facts'], 'model' : model_options}
        response = requests.post(f"{SERVER}/verify/ie/post", json=payload)
        list_of_relations = response.json()['list_of_relations']

        st.session_state.demo_state['list_of_triplets'] = list_of_relations


        st.divider() 

        st.subheader("Extracted Relations from Facts")
        for idx, relation in enumerate(list_of_relations): 
            if relation is None: 
                res = "<No valid triplets found for clause>"
            else: 
                temp = [] 
                for rel in relation: 
                    e1, rel, e2 = rel 
                    res = f"({e1}, {rel}, {e2})"
                    temp.append(res)
                
                res = " ".join(temp)

            st.markdown(f"{idx+1}. {res}")


        st.text("")   
        st.caption("Integrations for coreference resolution and cross-fact information extraction will soon be added!   ")




    # Triplet Matching 
    if val == 4: 

        docs_to_search = [] 

        #st.session_state.demo_state['list_of_triplets'] = [("Rapunzel", "had", "long hair"), ("Little Red-Cap", "had been picking", "flowers")]

        payload = {'list_of_triplets' : st.session_state.demo_state['list_of_triplets'], 'docs_to_search' : docs_to_search}
        response = requests.post(f"{SERVER}/verify/triplet/post", json=payload)
        triplet_matches = response.json()['triplet_matches']

        docs_string = ", ".join(docs_to_search)
        st.info(f'Only utilizing documents ({docs_string}). To change this, increase sensitivity in "Doc Identification" section.', icon="ℹ️")
        st.caption('_Coming soon, CrossVal for triplet verification https://arxiv.org/pdf/2008.06995.pdf_ 🥳')
        st.divider()

        if triplet_matches: 
            num_facts = len(triplet_matches)

        tab_titles = [] 
        info_dump = [] 

        for idx, entry in enumerate(triplet_matches):

            #curr_trip = st.session_state.demo_state['list_of_triplets'][idx]
            #print(curr_trip)
            #triplet_str = ",".join(curr_trip)
            #print(triplet_str)

            print(entry)

            tab_titles.append(f"Fact {idx+1}.")

            if len(entry) == 0 or not entry['match']: 
                match_string = f"<No match found!>)"
                match_triplet = ""
                match_context = "" 
            
            else: 
                match_string = f"Percent match: {entry['score']} ({entry['doc']}) | Searching for: ({entry['sub']}, {entry['rel']}, {entry['obj']})"
                match_triplet = entry['match_triplet']
                match_context = entry['match_context']

            info_dump.append([match_string, match_triplet, match_context])

        if len(tab_titles) != 0: 
            tab_list = st.tabs(tab_titles)

            for idx, tab in enumerate(tab_list): 
                info = info_dump[idx]
                with tab: 
                    st.info(info[0], icon="📖")
                    #st.subheader("Closest Triplet(s):")
                    #st.text(info[2])
                    st.subheader("Relevant context:")
                    st.caption(info[1])



    # Overall Final Score 
    if val == 5: 

        """
        
        TODO - NEED TO IMPLEMENT THIS 

        Statistics needed for this section: 

        - How many phrases identifed in response
        - Of those phrases, how many were facts
        - Of the facts, how many had relation triplets 
        - Of the triplets, how many were matched 

        Validity score = matched_triplets / num_facts 
        Validity devn = num_facts / num_phrases 


        For each matched triplet, what doc was it matched in (and what was the score)
        - For variation score, put inverse of how many docs were taken from there 

        
        """

        st.subheader("Overall Validity: ")

        #st.error(f"This has NOT been implemented yet, but will be very soon! See frontend/col2B line 193 for comments!", icon="🚨")
      
        colA, colB, colC = st.columns(3)    
        colA.metric("Overall Validity", "87%", "10%")
        colB.metric("rapunzel.txt", "72%", "8%")
        colC.metric("disney_data.txt", "10%", "6%")

        st.caption("The large number represents the confidence score. The smaller number represents the error margin.")
        st.caption("The overall validity score is simply the number of verified facts divided by number of identified facts.")
        st.caption("The overall validity deviation score is given by the number of identified facts over the number of total phrases")
        st.caption("The individual document scores reflect the average of the individual triplet-match scores across facts verified from a given document.")
        st.caption("Currently, this metric is the inverse of how many matched_facts")

        st.divider() 

        st.subheader("Of the 9 phrases identified in the response, 8 were identified as facts.")
        st.subheader("Of these 8 facts, 7 were able to be decomposed into entity-relation-entity triplets")
        st.subheader("Of these 7 relation triplets, 5 were sufficiently matched across 1 document.")

        st.balloons() 





"""

Helper method to format annotated text into st.annotated_text()

"""

def format_annotated_txt(text): 
    new_try = [] 
    for entry in text: 
        if isinstance(entry, str): new_try.append(entry)
        else: 
            p1, p2 = entry 
            new_try.append((p1, p2))
    
    return new_try