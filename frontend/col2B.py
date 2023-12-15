
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


import requests 
import streamlit as st 
from annotated_text import annotated_text 
import extra_streamlit_components as stx

from const import TAB_TITLES, SERVER


#  'verify_metrics' : {'num_phrases' : 0, 'num_facts' : 0, 'num_triplets' : 0, 'num_matched' : 0, 'docs_found_in' : {}}

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
            st.subheader(f"(User) {' '.join(st.session_state.demo_state['input_list_redacted'])}")
            st.divider()
            st.subheader(f"(LLMs) {' '.join(st.session_state.demo_state['output_list_exfiltrated'])}")

            st.markdown("")            
            for idx, elem in enumerate(st.session_state.demo_state['output_list_exfiltrated']):
                st.markdown(f"(Query {idx+1}) LLM Output: {elem}")
        


    # Doc Identification
    if val == 1: 
        st.subheader("Exfiltration Check on Documents in Knowledge Base.")

        if st.session_state.demo_state['any_leak']: 
            st.error('Data leak detected', icon="🚨")
            for idx, doc_match_per_prompt in enumerate(st.session_state.demo_state['leak_list']): 
                if doc_match_per_prompt or len(doc_match_per_prompt) > 0: 
                    # Print out the doc w/ the highest match score (the first entry, idx 0)
                    st.error(f"(Query {idx+1}) Document Name: {doc_match_per_prompt[0]}", icon="🚨")

        else:
            st.success("No information was leaked", icon="✅")
        
        st.divider() 
        
        with st.spinner('Determining Topics...'):

            # TODO - Here, need to add the data exfiltration stuff (Raunak already has a function for this!!)

            payload = {'input' : st.session_state.demo_state['input_list_redacted'], 'output' : st.session_state.demo_state['output_list_exfiltrated']}

            response = requests.post(f"{SERVER}/exfiltrator/topic/post", json=payload) # TODO - add this in! 
            st.session_state.demo_state['input_topic_list'] = response.json()['input_topic_list'] 
            st.session_state.demo_state['output_topic_list'] = response.json()['output_topic_list'] 

            print(f"Input Topics: {st.session_state.demo_state['input_topic_list']}")
            print(f"Output Topics: {st.session_state.demo_state['output_topic_list']}")

            colX, colY = st.columns(2)
            doc_list = []

            with colX: 
                st.subheader(f"Prompt Documents: ")
                for entry in st.session_state.demo_state['input_topic_list']: 
                    if len(entry) > 0: 
                        for res in entry: 
                            doc_list.append(res[0])
                            st.text(f" - {res[0]} ~ {res[1]}")

            with colY: 
                st.subheader(f"Response Documents:")
                if len(st.session_state.demo_state['output_topic_list']) > 0: 
                    for entry in st.session_state.demo_state['output_topic_list']: 
                        for res in entry: 
                            doc_list.append(res[0])
                            st.text(f" - {res[0]} ~ {res[1]}")

            st.session_state.demo_state['triplet_doc_list'] = doc_list

            st.text("")
            st.caption("The 'score' is the distance, meaning lower = better match!")

    #Fact vs. Opinion Classifier 
    if val == 2: 
        if st.session_state.demo_state['any_leak']: 
            st.error(f"Part of the LLM response may have been removed due to Data Exfiltration leakage.", icon="🚨")

        # TODO - need to somehow specify which docs to check against, based on step previously 
        # TODO - ideally, we'd like to only check documents relevant to each subprompt/suboutput 

        payload = {'output_list' : st.session_state.demo_state['output_list_exfiltrated']}
        response = requests.post(f"{SERVER}/verify/facts/post", json=payload)

        st.session_state.demo_state['list_of_facts'] = response.json()['list_of_facts']
        st.session_state.demo_state['verify_metrics']['num_phrases'] = response.json()['num_phrases']
        st.session_state.demo_state['verify_metrics']['num_facts'] = len(st.session_state.demo_state['list_of_facts'])

        st.subheader("Labelling with Fact-vs-Opinion Classifier")
        annotated_text(format_annotated_txt(response.json()['annotated_txt']))

        st.divider()

        st.subheader(f"Extracted {st.session_state.demo_state['verify_metrics']['num_facts'] } facts from LLM Response:")
        for idx, fact in enumerate(st.session_state.demo_state['list_of_facts']): 
            st.markdown(f"{idx+1}. {fact}")


    """
    
    TODO - Previously, used to be AMR code here. This old code has been saved and will eventually be added. 

    #st.graphviz_chart(st.session_state.demo_state['amr_grp_inp'])        
    #st.graphviz_chart(st.session_state.demo_state['amr_grp_out'])
    
    """
    
    # Information Extraction
    if val == 3: 
        model_options = st.selectbox('Please select an Information Extraction (IE) method. Default methodology, Stanford OpenIE.', ["Stanford OpenIE"]) # TODO - Add in UIUC AMR-IE support 

        payload = {'list_of_facts' : st.session_state.demo_state['list_of_facts'], 'model' : model_options}
        response = requests.post(f"{SERVER}/verify/ie/post", json=payload)
        st.session_state.demo_state['list_of_relations'] = response.json()['list_of_relations']

        st.divider() 

        num_triplets = len([item for item in st.session_state.demo_state['list_of_relations'] if item is not None])
        st.session_state.demo_state['verify_metrics']['num_triplets'] = num_triplets 
        st.subheader(f"Extracted {num_triplets} Relations from Facts")

        for idx, relation in enumerate(st.session_state.demo_state['list_of_relations']): 
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
        st.caption("Integrations for coreference resolution and cross-fact information extraction will soon be added!")




    # Triplet Matching 
    if val == 4: 
        # TODO - if there are NO docs to search, endpoint should search ALL the code 
        payload = {'list_of_relations' : st.session_state.demo_state['list_of_relations'], 'docs_to_search' : st.session_state.demo_state['triplet_doc_list']}
        response = requests.post(f"{SERVER}/verify/triplet/post", json=payload)
        triplet_matches = response.json()['triplet_matches']
        # TODO - move num_matched and docs_found_in calculations into gateway backend 

        docs_string = ", ".join(st.session_state.demo_state['triplet_doc_list'])
        st.info(f'Only utilizing documents ({docs_string}). To change this, modify sensitivity in gateway/admin.yml.', icon="ℹ️")
        st.caption('Please note that Triplet Matching can be quite finnicky/sensitive. Improvements to come!')
        st.caption('_Coming soon, CrossVal for triplet verification https://arxiv.org/pdf/2008.06995.pdf_ 🥳')
        st.divider()

        tab_titles = [] 
        info_dump = [] 

        num_matched = 0 
        docs_found_in = {}

        for idx, entry in enumerate(triplet_matches):
            print(f"(col2B) Triplet Matching Entry: {entry}")

            tab_titles.append(f"Fact {idx+1}.")

            if len(entry) == 0 or not entry['match']: 
                match_string = f"<No match found!>)"
                match_triplet = ""
                match_context = "" 
            
            else: 
                match_string = f"Percent match: {entry['score']} ({entry['doc']}) | Searching for: ({entry['sub']}, {entry['rel']}, {entry['obj']})"
                match_triplet = entry['match_triplet']
                match_context = entry['match_context']
                
                num_matched += 1 
                if entry['doc'] in docs_found_in: 
                    docs_found_in[entry['doc']] += 1 
                else: 
                    docs_found_in[entry['doc']] = 1 


            info_dump.append([match_string, match_triplet, match_context])


        st.session_state.demo_state['verify_metrics']['num_matched'] = num_matched
        st.session_state.demo_state['verify_metrics']['docs_found_in'] = docs_found_in

        if len(tab_titles) != 0: 
            tab_list = st.tabs(tab_titles)

            for idx, tab in enumerate(tab_list): 
                info = info_dump[idx]
                with tab: 
                    st.info(info[0], icon="📖")
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

        num_phrases = st.session_state.demo_state['verify_metrics']['num_phrases']
        num_facts = st.session_state.demo_state['verify_metrics']['num_facts']
        num_triplets = st.session_state.demo_state['verify_metrics']['num_triplets']
        num_matched = st.session_state.demo_state['verify_metrics']['num_matched']
        docs_found_in = st.session_state.demo_state['verify_metrics']['docs_found_in']
        # Remember, docs_found_in is a dict in the format {'doc_name' : 'num_facts_found_in_this_doc'}

        print(f"(col2B) Verify Metrics: {st.session_state.demo_state['verify_metrics']}")

        inverted_list = [] 
        for item, freq in docs_found_in.items():
            inverted_list.append((freq, item))

        print(f"(col2B) Inverted List: {inverted_list}")

        # Now, we have an inverted, sorted dictionary in format {'num_facts_found' : 'doc_name'}

        sorted_inverted_list = sorted(inverted_list, key=lambda x: x[0])
        formatted_doc_list = [[item, f"{freq} facts", round(freq / num_matched * 100, 1) if num_matched != 0 else None] for freq, item in sorted_inverted_list]


        scores = {
            'overall_val' : round(num_matched / num_facts * 100, 1) if num_facts != 0 else None, 
            'overall_dev' : round(num_facts / num_phrases * 100, 1) if num_facts != 0 else None, 
        }

        st.subheader("Overall Validity: ")
        print(f"(col2B) Docs found in: {st.session_state.demo_state['verify_metrics']['docs_found_in']}")
        print(f"(col2B) Formatted doc list: {formatted_doc_list}")

        cols = st.columns(len(st.session_state.demo_state['verify_metrics']['docs_found_in']) + 1)   
        for idx, col in enumerate(cols): 
            if idx == 0: 
                col.metric("Overall Validity", f"{scores['overall_val']}%", f"{scores['overall_dev']}")
            else: 
                res = formatted_doc_list[idx-1]
                print(f"(col2B) Res: {res}")
                col.metric(res[0], res[1], res[2])

        st.caption("The large number represents the confidence score. The smaller number represents the error margin.")
        
        st.caption("The overall validity score is simply the number of verified facts divided by number of identified facts.")
        st.caption("The overall validity deviation score is given by the number of identified facts over the number of total phrases")

        st.caption("The individual document scores reflect the average of the individual triplet-match scores across facts verified from a given document.")

        st.divider() 

        st.subheader(f"Of the {num_phrases} phrases identified in the response, {num_facts} were identified as facts.")
        st.subheader(f"Of these {num_facts} facts, {num_triplets} were able to be decomposed into entity-relation-entity triplets")
        st.subheader(f"Of these {num_triplets} relation triplets, {num_matched} were sufficiently matched across {len(docs_found_in)} documents.")

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