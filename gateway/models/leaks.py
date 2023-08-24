import faiss
import pickle
import numpy as np
import pandas as pd
import os

from rannet import RanNet, RanNetWordPieceTokenizer

class ExfiltrationModel(): 

    def __init__(self, file_list = None, data_folder_path = None): 

        """
        
        TODO - look at docs/, preprocess them into vectors in index path 
        - Don't do this for all the files, just select "high-security" ones (1 or 2)
        
        """

        EXFILTRATION_PATHS = {
            'vocab_path' :  './models/rannet-base-v2-en-uncased-model/vocab.txt', 
            'ckpt_path' : './models/rannet-base-v2-en-uncased-model/model.ckpt', 
            'config_path' : './models/rannet-base-v2-en-uncased-model/config.json', 
            'my_data_frame' : './models/rannet_store/my_data_frame.pkl', 
            'vectors' : './models/rannet_store/vectors.pkl', 
            'index' : './models/rannet_store/index.pkl'
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

        """ Check for files in docs """
        directory_path = data_folder_path
        files = os.listdir(directory_path)
        for i in files:
            if i[0] != ".":
                file_name = (i.split(".")[0])
                if file_name not in list(self.my_data_frame['category']):
                    file = open(directory_path+i)
                    text_input = file.read()
                    
                    """ Adding to my_data_frame """
                    new_row = pd.DataFrame({'category': file_name, 'text': text_input}, index=[0])
                    self.my_data_frame = pd.concat([self.my_data_frame.loc[:], new_row]).reset_index(drop=True)

                    """ Adding to vector """
                    tok = self.tokenizer.encode(text_input)
                    vec = self.rannet_model.predict(np.array([tok.ids]))
                    self.vectors.append(vec) 
                    
                    """ Adding to index """
                    my_vector = np.array(self.vectors)
                    my_vector = np.squeeze(my_vector)
                    vector_dimension = self.vectors[0].shape[1]
                    self.index = faiss.IndexFlatL2(vector_dimension)
                    faiss.normalize_L2(my_vector)
                    self.index.add(my_vector)

        """ Check if the sensitive file-list is empty"""
        EXFILTRATION_CONSTS['file_list'] = file_list

        self.filter_list = EXFILTRATION_CONSTS['file_list']
        self.top_k = EXFILTRATION_CONSTS['top_k']
        
        """ For quick test """
        # sample_text = "A dog breed will consistently produce the physical traits, movement and temperament that were developed over decades of selective breeding. For each breed they recognize, kennel clubs and breed registries usually maintain and publish a breed standard which is a written description of the ideal specimen of the breed.[2][3][4] Other uses of the term breed when referring to dogs include pure breeds, cross-breeds, mixed breeds and natural breeds.[5]"
        # a = self.detect_leak(sample_text)
        # print (a)


    def query_based_on_distance(self, search_text, index, vec, my_data_frame):
        #return  
        # Creating embedding vectors
        tok = self.tokenizer.encode(search_text)
        vec = self.rannet_model.predict(np.array([tok.ids]))
        faiss.normalize_L2(vec)
        
        
        k = 50
        print ("here",k)
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
