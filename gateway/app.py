from flask import Flask, request
import json
import os
import copy
import yaml

from models.model import Model 
from models.cache import QACache 
from models.prompt import QueryProcessor 
from models.leaks import ExfiltrationModel
from models.verify import VerificationModel 



def simple_parse(combos):
    queries = combos.split('? ')
    for i in range(len(queries) - 1):
        queries[i] += "?"
    return queries


def create_server_state():
    state = {} 
    return state 


def create_app(server_state):

    """ Reading YAML """
    with open('admin.yml', 'r') as file:
        config_setup = yaml.safe_load(file)
    
    
    app = Flask(__name__)
    initial_server_state = copy.deepcopy(server_state)


    """ Initiating """
    
    llm_models = Model(config_setup['supported_models'], config_setup['api_keys']) 

    processor = QueryProcessor()
    
    qa_cache = QACache(data_folder_path=config_setup['path_to_doc'], 
                       api_keys=config_setup['api_keys'])

    exfiltrator = ExfiltrationModel(file_list=config_setup['sensitive_info'], 
                                    data_folder_path=config_setup['path_to_doc']) 
    
    verifier = VerificationModel(fact_threshold=config_setup['fact_threshold'],
                                 fact_model_name=config_setup['fact_model_name'], 
                                 rel_threshold=config_setup['rel_threshold'])  

    
    """ 00) General Methods """

    # / - Ensure Working API Server
    @app.route('/', methods=['GET'])
    def default():
        nonlocal server_state
        return {'response': "Working API server"}, 200


    # /reset - Reset server state (TODO: not user)
    @app.route('/reset', methods=['GET'])
    def reset():
        server_state = initial_server_state
        return {'response': "Reset Successful"}, 200


    # /docs - Return documents in Knowledge Base 
    @app.route('/docs', methods=['GET'])
    def docs():
        file_list = []
        
        for filename in os.listdir(config_setup['path_to_doc']):
            # TODO - Currently only supports text files! 
            if filename.endswith(".txt"):
                filepath = os.path.join(config_setup['path_to_doc'], filename)
                if os.path.isfile(filepath):
                    size_kb = os.path.getsize(filepath) / 1024  
                    file_list.append((filename, round(size_kb, 4)))
        
        return {'docs': file_list, 'path' : config_setup['path_to_doc'], 'show' : config_setup['show_docs']}, 200


    # /model_list - Return list of Models 
    @app.route('/model_list', methods=['GET'])
    def models():        
        model_list = config_setup['supported_models']
        return {'model_list': model_list}, 200


    # /model --> receives prompt, llm, and returns specified llm answer 
    @app.route('/model', methods=['POST'])
    def model_post():
        nonlocal server_state
        data = request.get_json()

        resp = llm_models.generate(data['llm'], data['prompt'])
        return json.dumps({'general_res' : resp})



    """ 01) Input Layer Methods """

    # /prompt/post --> receives prompt, selected models and returns cost options, redacted, split 
    @app.route('/prompt/post', methods=['POST'])
    def prompt_post():
        nonlocal server_state

        data = request.get_json()
        text = data['prompt']
        llms = data['llms']

        input_list = processor.decompose_query(text)
        input_list_redacted = processor.redact_query_list(input_list) 
        print("(app /prompt/post) About to modify input for prompt")
        input_list_injected = processor.modify_input_for_prompt(input_list_redacted)
        print(f"(app /prompt/post) Injected Prompt List: {input_list_injected}")
        # TODO - change so get_combination_options uses the redacted list of queries instead of text 
        print("(app /prompt/post) About to get combination options")
        result = processor.get_combination_options(input_list_injected, llms) 
        return json.dumps({'input_list_injected' : input_list_injected, 
                            'input_list_redacted' : input_list_redacted, 
                            'input_list' : input_list, 
                            'cost_options' : result})


    # /cache/search/post --> receives prompt list, returns cache results 
    @app.route('/cache/search/post', methods=['POST'])
    def cache_search_post():
        nonlocal server_state
        data = request.get_json()

        prompt_list = data['prompt_list']

        cache_responses = []
        anythingFound = False 

        for elem in prompt_list:
            found, similar_q, response = qa_cache.search(elem)
            anythingFound = anythingFound or found
            if found:
                # TODO - Change this so we don't return the string, but actual match/response 
                cache_responses.append(f"Query ({elem}) matched ({similar_q}).\nCached response: {response}")
            else: 
                cache_responses.append(response)

        return json.dumps({'cache_results' : cache_responses, 'cache_found' : anythingFound})


    # /cache/model/post --> uses doc-specific LLM found in cache 
    @app.route('/cache/model/post', methods=['POST'])
    def cache_model_post():
        nonlocal server_state
        data = request.get_json()

        # TODO - only gpt-3.5 is implemented on docs
        if "gpt-3.5" not in data['llm']: 
            return json.dumps({'doc_specific_res' : None})

        # TODO - Do NOT add to cache here. Add after exfil check! 
        answer = qa_cache.get_answer(f"{data['prompt']} If you do not know, please return 'IDK'. ")
        if "IDK" in answer: answer = None 

        return json.dumps({'doc_specific_res': answer})


    # /cache/add/post --> adds (question, answer) to cache 
    @app.route('/cache/add/post', methods=['POST'])
    def cache_add_post():
        nonlocal server_state
        data = request.get_json()

        qa_cache.add_to_cache(data['prompt'], data['output'])
        return {'response': "Successfully added to cache."}, 200
   
    
    """ 02) Output Layer Methods """

    # /exfiltrator/post --> receives output, returns leaks, if any
    @app.route('/exfiltrator/post', methods=['POST'])
    def exfiltrator_post():
        nonlocal server_state
        data = request.get_json()

        leaks = [] 
        any_leak = False 
        exfiltrated = [] 

        for text in data['text_list']: 
            leak = exfiltrator.detect_leak(text)
            any_leak = leak or any_leak
            leaks.append(leak) 

            if leak: 
                exfiltrated.append("<DOC_EXFIL_FLAG>")
            else: 
                exfiltrated.append(text)

        return json.dumps({'output_list_exfiltrated' : exfiltrated, 'leak_list' : leaks, 'any_leak' : any_leak})



    # /exfiltrator/post --> receives output, returns leaks, if any
    @app.route('/exfiltrator/topic/post', methods=['POST'])
    def exfiltrator_topic_post():
        nonlocal server_state
        data = request.get_json()

        input_docs = [] 
        for text in data['input']: 
            input_docs.append(exfiltrator.detect_docs(text))

        output_docs = [] 
        for text in data['output']: 
            output_docs.append(exfiltrator.detect_docs(text))
          
        return json.dumps({'input_topic_list' : input_docs, 'output_topic_list' : output_docs})


    # /verify/facts/post --> receives output, returns facts, if any
    @app.route('/verify/facts/post', methods=['POST'])
    def verify_facts_post():
        nonlocal server_state
        data = request.get_json()

        list_of_facts, num_phrases, annotated_txt = verifier.fact_vs_opinion(data['output_list']) 
        return json.dumps({'list_of_facts' : list_of_facts, 'num_phrases' : num_phrases, 'annotated_txt' : annotated_txt})


    # /verify/ie/post --> receives list of facts, returns relations for each, if any
    @app.route('/verify/ie/post', methods=['POST'])
    def verify_ie_post():
        nonlocal server_state
        data = request.get_json() 

        list_of_facts = data['list_of_facts']
        model = data['model'] # TODO - currently not using 'model' (def StanfordOpenIE)

        list_of_relations = verifier.get_relations(list_of_facts, model) 
        return json.dumps({'list_of_relations' : list_of_relations})


    # /verify/triplet/post --> receives list of triplets, returns matches/info if found 
    @app.route('/verify/triplet/post', methods=['POST'])
    def verify_triplet_post():
        nonlocal server_state
        data = request.get_json()
    
        list_of_triplets = data['list_of_relations']
        docs = data['docs_to_search']

        res = verifier.match_triplets(list_of_triplets, docs) 
        return json.dumps({'triplet_matches' : res})


    return app


def run_app_server(app, port=3000, ip='localhost'):

    print("PID:", os.getpid())
    print("Werkzeug subprocess:", os.environ.get("WERKZEUG_RUN_MAIN"))
    print("Inherited FD:", os.environ.get("WERKZEUG_SERVER_FD"))
    app.run(host=ip, port=port)


if __name__=='__main__': 
    state = create_server_state() 
    app = create_app(state)

    run_app_server(app)