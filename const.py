# Constants File --> will eventually be imported from YML (BLAZE Integration)

""" 

Prompt layer Constants

"""

INITIAL_STATE =  {
        'select_llms' : None,

        'input_prompt' : None, 
        'output_resp' : None,

        'input_prompt_list' : [],
        'output_response_list' : [],
 
        'cost_options_ready' : False, 
        'cache_result_ready' : False, 

        'cost_options' : None, 
        'cache_result' : None, 
        'cache_found' : False, 

        'selected_generation' : False,
        
        'start_exfil' : None,
        'found_docs' : False, 
        'matched_docs' : None,
        'queries' : None, 

    }

LLM_OPTIONS = ['gpt-3.5', 'gpt-4', 'llama-2', 'dolly-3b', 'gptj-6b']

MODEL_COSTS = {
                "gpt-3.5-turbo": 0.06 / 1000,  # $0.06 per 1000 tokens
                "gpt-4": 0.08 / 1000  # $0.08 per 1000 tokens
            }

DUMMY_DOCS = ''' - corporate_01.txt
- corporate_02.txt
- corporate_03.txt
- corporate_04.txt'''

EXPANDER_TEXT = "Cost, Prompt, and Cache options will be shown in this expander. Please select an option by using the 'Proceed' button below. Feel free to hide me when you're finished."

#BASE_PROMPT = "What lesson did Hansel and Gretel teach to children, and how is this similar to the lesson taught by the princess locked in the tower"
BASE_PROMPT = ""

RADIO_ITEMS = "The default option has been preselected. Combinations and options are shown below."

INPUT_SUCCESS = "Results of Prompt and Cache Layer are discussed to the right!"

SERVER = "http://localhost:3000"

"""

Cache layer Constants

"""


"""

Exfiltration layer Constants

"""

EXFILTRATION_PATHS = {
    'vocab_path' :  './models/rannet-base-v2-en-uncased-model/vocab.txt', 
    'ckpt_path' : './models/rannet-base-v2-en-uncased-model/model.ckpt', 
    'config_path' : './models/rannet-base-v2-en-uncased-model/config.json', 
    'my_data_frame' : './models/rannet_store/my_data_frame_50.pkl', 
    'vectors' : './models/rannet_store/vectors_50.pkl', 
    'index' : './models/rannet_store/index_50.pkl'
}

EXFILTRATION_CONSTS = {
    'file_list' : ['Dutch_Republic', 'Symbiosis', 'Heresy', 'Hunter-gatherer', 'Pub'], 
    'top_k' : 5
}


SENSITIVITY_SLIDER_TEXT = "Sensitivity of Document Embeddings (top-k, 1 = strict, 4 = flexible). Default selection is 2, meaning top-2 documents are chosen for both prompt and response 🔎."


"""

Verification layer Constants

"""


#SQUAD_TITLES = ['1973 Oil Crisis', 'Black Death', 'Amazon Rainforest', 'Ctenophora', 'Warsaw']

TAB_TITLES = ["Base I/O", "Doc Identification", "Fact vs. Opinion", "Relation Extraction", "Triplet Matching", "Final Statistics"]

#BASE_PROMPT = "What caused the 1973 oil crisis to begin?"
#BASE_PROMPT = "How did the Nixon administration negotiate with the uncooperative countries during the 1973 Oil Crisis?"
#BASE_PROMPT = "What lesson did Hansel and Gretel teach to children?"

#DUMMY_ANS = "To address this, the Nixon Administration began multilateral negotiations with the combatants. They arranged for Israel to pull back from the Sinai Peninsula and the Golan Heights."
#DUMMY_ANS = "Oil supply is a flexible supply which reacts to economic and political changes rapidly. The international oil price shocks of 1973 and 1979 to 1980 were one of the major economic shocks that oil producing countries experienced. The sudden increase in cost caused by supply disruptions of these oil price shocks resulted in a change in consumer behavior and an overall price increase across the oil consuming economy. These price increases lead to a reduction in the consumption of oil which cause a reduction in the supply of oil supply and creates a negative economic feedback loop."

#DUMMY_ANS = """Hansel and Gretel teaches children to be resourceful and brave in adversity, using breadcrumbs to find their way back and outwitting the witch. It also warns against greed and the consequences of trusting strangers."""
#DUMMY_ANS = """Hansel and Gretel teaches children the value of family bonds, as the siblings support and protect each other throughout their journey. The tale warns against trusting strangers blindly, as the wicked witch lures the children with her candy-coated house, revealing the dangers of deceitful individuals. The children's use of breadcrumbs as a trail reflects the importance of planning and foresight in difficult situations, showing the significance of being prepared. Similarly, the princess locked in the tower, like Rapunzel, showcases resilience and patience while using her long hair as a resource to aid her escape, emphasizing the power of adaptability and ingenuity."""
DUMMY_ANS = """5 + 5 is 10. Symbiosis is a major thing involving Symbiosis which has the word Bio in it because Symbiosis."""


FACTS = ["the siblings support and protect each other throughout their journey", "the wicked witch lures the children with her candy-coated house", "The children's use of breadcrumbs as a trail", "the princess locked in the tower, like Rapunzel", "using her long hair as a resource to aid her escape"]