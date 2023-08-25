from elasticsearch import Elasticsearch
import spacy
import os 

# Initialize NLP tools
nlp = spacy.load("en_core_web_sm")

# Initialize Elasticsearch
es = Elasticsearch()


class ElasticVerification(): 

    def __init__(self, dir_path, files_list): 

        # TODO - need to take this from admin.yml 
        self.index_text_files(dir_path, files_list)


    # TODO - update so that it only looks at the documents GIVEN to it NOT All! 

    # (Helper) Index Text Files 
    def index_text_files(self, directory_path, files_list):
        for filename in os.listdir(directory_path):

            # TODO - Only handling text files, at the moment!
            if filename.endswith(".txt"):
                # TODO - Once looking at given docs, can remove "not files_list" check 
                if not files_list or (filename.split(".")[0]) in files_list: 
                    with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                        content = file.read()
                        doc = nlp(content)
                        sentences = [sent.text for sent in doc.sents]
                        for i, sentence in enumerate(sentences):
                            es.index(index="text_index", id=f"{filename}_{i}", body={"text": sentence, "file": filename, "index": i})



    # (Helper) Search for matches
    def search_for_matches(self, query):
        res = es.search(index="text_index", body={"query": {"match": {"text": query}}, "min_score": 6.5})
        return res['hits']['hits']


    # The main function being called 
    def triplet_match(self, triplet, docs): 

        subject, relation, obj = triplet 

        query = f"{subject} {relation} {obj}"
        matches = self.search_for_matches(query)
        if matches: 
            print(f"   Got {len(matches)}")

        for match in matches:
            score = match['_score']
            matched_text = match['_source']['text']
            file_name = match['_source']['file']
            index = match['_source']['index']
            context = " ".join(matched_text.split()[:10])  # Get the first few words as context
            print(f"Query: {query}")
            print(f"Confidence Score: {score}")
            print(f"Matched Document: {file_name} (Index: {index})")
            print(f"Matched Triplet: {subject}, {relation}, {obj}")
            print(f"Context: {context}")
            print("=" * 50)

            return True, score, file_name, matched_text, context
        
        return False, 0.0, None, None, None 


