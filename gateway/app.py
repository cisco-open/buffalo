from flask import Flask, request
import json
import os
import copy

from models.model import Model 
from models.cache import QACache 
from models.prompt import QueryProcessor 
from models.leaks import ExfiltrationModel
from models.verify import VerificationModel 
import yaml


def simple_parse(combos):
    queries = combos.split('? ')
    for i in range(len(queries) - 1):
        queries[i] += "?"
    return queries


def create_server_state():
    state = {} 
    return state 


def create_app(server_state):
    """
    Reading YAML
    """
    with open('admin.yml', 'r') as file:
        config_setup = yaml.safe_load(file)
    
    
    app = Flask(__name__)
    initial_server_state = copy.deepcopy(server_state)
    print("(create_app) > Server state is ", server_state)

    """ Initiating """
    llm_model = Model() 

    processor = QueryProcessor()
    qa_cache = QACache()
    
    print (config_setup['sensitive_info'])
    exfiltrator = ExfiltrationModel(file_list=config_setup['sensitive_info'], data_folder_path=config_setup['path_to_doc']) 
    verifier = VerificationModel()  

    DOCS_PATH = ".\docs"

    
    """
    
    00) General Methods
    
    """

    @app.route('/', methods=['GET'])
    def default():
        nonlocal server_state
        return {'response': "Working API server"}, 200


    @app.route('/reset', methods=['GET'])
    def reset():
        server_state = initial_server_state
        return {'response': "Reset Successful"}, 200


    @app.route('/docs', methods=['GET'])
    def docs():
        file_list = []
        
        for filename in os.listdir(DOCS_PATH):
            if filename.endswith(".txt"):
                filepath = os.path.join(DOCS_PATH, filename)
                if os.path.isfile(filepath):
                    size_kb = os.path.getsize(filepath) / 1024  
                    file_list.append((filename, round(size_kb, 4)))
        
        return {'docs': file_list}, 200



    """
    
    01) Input Layer Methods 
    
    """

    # /prompt/post --> receives prompt, selected models and returns cost options 

    @app.route('/prompt/post', methods=['POST'])
    def prompt_post():
        nonlocal server_state

        data = request.get_json()
        text = data['prompt']
        llms = data['llms']

        result = processor.get_combination_options(text, llms) 
        print("(app) Cost Option Results", result)

        return json.dumps({'cost_options' : result})


    # /cache/post --> receives prompt, returns cache results 

    @app.route('/cache/post', methods=['POST'])
    def cache_post():
        nonlocal server_state

        data = request.get_json()
        text = data['prompt']
        llms = data['llms']

        add = bool(data['add'])
        threshold = float(data['threshold'])

        queries = simple_parse(text)
        cache_responses = []

        anythingFound = False 

        print("CACHE QUESTIONS", qa_cache.questions)

        for elem in queries:
            found, similar_q, response = qa_cache.search(elem, add=add, threshold=threshold)
            if found:
                cache_responses.append("Your query: (" + elem + ") was deemed similar to: " + similar_q + ". Here is the response: " + response)
            else: 
                cache_responses.append(response)
            
            anythingFound = anythingFound or found

        result = cache_responses
        print("(app) Cache Search", result)

        return json.dumps({'cache_results' : result, 'queries' : queries, 'cache_found' : anythingFound})


    """
    
    02) Output Layer Methods
    
    """

    # /exfiltrator/post --> receives output, returns leaks, if any

    @app.route('/exfiltrator/post', methods=['POST'])
    def exfiltrator_post():
        nonlocal server_state

        data = request.get_json()
        text = data['text']

        result = exfiltrator.detect_leak(text) 
        print("(app) Cost Option Results", result)

        return json.dumps({'leak' : result})


    # /verify/facts/post --> receives output, returns facts, if any

    @app.route('/verify/facts/post', methods=['POST'])
    def verify_facts_post():
        nonlocal server_state

        data = request.get_json()
        text = data['text']

        list_of_facts, annotated_txt = verifier.fact_vs_opinion(text) 

        print("(app) List of Facts Results", list_of_facts)
        print("(app) Annotated Txt Results", annotated_txt)

        return json.dumps({'list_of_facts' : list_of_facts, 'annotated_txt' : annotated_txt})


    # /verify/ie/post --> receives list of facts, returns relations for each, if any

    @app.route('/verify/ie/post', methods=['POST'])
    def verify_ie_post():
        nonlocal server_state

        data = request.get_json()
        list_of_facts = data['list_of_facts']
        model = data['model']

        list_of_relations = verifier.get_relations(list_of_facts, model) 
        print("(app) List of Relations Results", list_of_relations)

        return json.dumps({'list_of_relations' : list_of_relations})



    # /verify/triplet/post --> receives list of triplets, returns matches/info if found 

    @app.route('/verify/triplet/post', methods=['POST'])
    def verify_triplet_post():
        nonlocal server_state

        data = request.get_json()
        list_of_triplets = data['list_of_triplets']
        docs = data['docs_to_search']

        res = verifier.match_triplets(list_of_triplets, docs) 
        print("(app) List of Relations Results", res)

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