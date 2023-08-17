import faiss
import pickle
import numpy as np
import pandas as pd

from rannet import RanNet, RanNetWordPieceTokenizer

class ExfiltrationModel(): 

    def __init__(self): 

        """
        
        TODO - look at docs/, preprocess them into vectors in index path 
        - Don't do this for all the files, just select "high-security" ones (1 or 2)
        
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

        # Loading data store
        vocab_path = EXFILTRATION_PATHS['vocab_path']
        ckpt_path = EXFILTRATION_PATHS['ckpt_path']
        config_path = EXFILTRATION_PATHS['config_path']

        self.tokenizer = RanNetWordPieceTokenizer(vocab_path, lowercase=True)
        self.rannet, self.rannet_model = RanNet.load_rannet(
            config_path=config_path,
            checkpoint_path=ckpt_path,
            return_sequences=False,
            apply_cell_transform=False,
            cell_pooling='mean'
        )

        self.filter_list = EXFILTRATION_CONSTS['file_list']
        self.top_k = EXFILTRATION_CONSTS['top_k']



        # Load data store
        file = open(EXFILTRATION_PATHS['my_data_frame'], 'rb')
        self.my_data_frame = pickle.load(file)
        file.close()

        file = open(EXFILTRATION_PATHS['vectors'], 'rb')
        self.vectors = pickle.load(file)
        file.close()

        file = open(EXFILTRATION_PATHS['index'], 'rb')
        self.index = pickle.load(file)
        file.close()


    def query_based_on_distance(self, search_text, index, vec, my_data_frame):
        #return  
        # Creating embedding vectors
        tok = self.tokenizer.encode(search_text)
        vec = self.rannet_model.predict(np.array([tok.ids]))
        faiss.normalize_L2(vec)
        
        
        k = index.ntotal
        distances, ann = index.search(vec, k=k)
        
        results = pd.DataFrame({'distances': distances[0], 'ann': ann[0]})
        
        merge = pd.merge( results, my_data_frame, left_on='ann',right_index=True)        
        return merge


    def generate_response(self, txt):
        #return 
        merge = self.query_based_on_distance(txt, self.index, self.vectors, self.my_data_frame)
        return merge
    

    # txt is the input text, filter_list is the list of documents
    def detect_leak(self, txt): 
        #return  
        print("inputted txt", txt)
        response = self.generate_response(txt)
        result = [response]

        matched_docs = [] 

        if len(result): 
            response = result[0]

            distance = list(response['distances'])[:self.top_k]
            category = list(response['category'])[:self.top_k]

            if list(set(self.filter_list) & set(category)): 
                for i,j in zip(distance, category):
                    if j in self.filter_list:
                        matched_docs.append(j)
                
        return matched_docs
