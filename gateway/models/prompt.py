import re
from nltk.tokenize import sent_tokenize
class QueryProcessor:
    def __init__(self):
        self.MODEL_COSTS = {
            "gpt-3.5-turbo": 0.06 / 1000,  # $0.06 per 1000 tokens
            "gpt-4": 0.08 / 1000  # $0.08 per 1000 tokens
        }

    # TODO - THE REDACT METHODS MAY OR MAY NOT BE BEING CALLED -- DOUBLE CHECK THIS! 
    # TODO - can use external library (ex microsoft presidio)

    @staticmethod
    def redact_phone(s):
        phone_pattern = r'\b(\+\d{1,3}[-.]?)?(\()?(\d{3})(?(2)\))[-. ]?\d{3}[-.]?\d{4}\b'
        if re.search(phone_pattern, s):
            s = re.sub(phone_pattern, '**(Redacted Phone Num)**', s)
            return True, s
        else:
            return False, s
        
    @staticmethod
    def redact_ssn(s):
        ssn_pattern = r'\b\d{3}-?\d{2}-?\d{4}\b'
        if re.search(ssn_pattern, s):
            s = re.sub(ssn_pattern, '**(Redacted SSN)**', s)
            return True, s
        else:
            return False, s
        
    @staticmethod
    def redact_email(s):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.search(email_pattern, s):
            s = re.sub(email_pattern, '**(Redacted Email)**', s)
            return True, s
        else:
            return False, s

    @staticmethod
    def decompose_query(query):
        return sent_tokenize(query)


    def calculate_cost(self, text, model):
        tokens = len(text)
        return round(tokens * self.MODEL_COSTS[model], 5)
    

    def get_combination_options(self, query, model_list):
        decomposed_queries = self.decompose_query(query)

        # Initialize costs with an empty combination
        costs = [{"combo": [], "cost": 0.0}]

        for i, decomposed_query in enumerate(decomposed_queries):
            new_costs = []
            
            for cost_info in costs:
                for model in self.MODEL_COSTS:
                    new_combination = cost_info["combo"] + [(model, decomposed_query)]
                    new_cost = cost_info["cost"] + self.calculate_cost(decomposed_query, model)
                    new_costs.append({"combo": new_combination, "cost": new_cost})
            
            costs = new_costs

        costs.sort(key=lambda x: x["cost"])
        return costs
    #User specifies how many options they want to see. If n is 1 they will see the cheapest option, if n is 2 they will see the cheapest and most expensive poption, if n > 2 they will see the cheapest, most expensive, and n - 2 next cheapest
    def filter_results(self, costs, n):
        if n >= len(costs):
            return costs
        if n < 1:
            return []
        elif n == 1:
            return costs[0]
        elif n == 2:
            return [costs[0], costs[len(costs) - 1]]
        else:
            return [costs[0:n-1] + [costs[len(costs) - 1]]]




   

    








# import re
# from nltk.tokenize import sent_tokenize
# class QueryProcessor:

#     def __init__(self):
#         self.MODEL_COSTS = {
#             "gpt-3.5-turbo": 0.06 / 1000,  # $0.06 per 1000 tokens
#             "gpt-4": 0.08 / 1000  # $0.08 per 1000 tokens
#         }

#     # TODO - THE REDACT METHODS MAY OR MAY NOT BE BEING CALLED -- DOUBLE CHECK THIS! 
#     # TODO - can use external library (ex microsoft presidio)

#     @staticmethod
#     def redact_phone(s):
#         phone_pattern = r'\b(\+\d{1,3}[-.]?)?(\()?(\d{3})(?(2)\))[-. ]?\d{3}[-.]?\d{4}\b'
#         if re.search(phone_pattern, s):
#             s = re.sub(phone_pattern, '**(Redacted Phone Num)**', s)
#             return True, s
#         else:
#             return False, s
        
#     @staticmethod
#     def redact_ssn(s):
#         ssn_pattern = r'\b\d{3}-?\d{2}-?\d{4}\b'
#         if re.search(ssn_pattern, s):
#             s = re.sub(ssn_pattern, '**(Redacted SSN)**', s)
#             return True, s
#         else:
#             return False, s
        
#     @staticmethod
#     def redact_email(s):
#         email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
#         if re.search(email_pattern, s):
#             s = re.sub(email_pattern, '**(Redacted Email)**', s)
#             return True, s
#         else:
#             return False, s

#     @staticmethod
#     def decompose_query(query):
#         return sent_tokenize(query)


#     def calculate_cost(self, text, model):
#         tokens = len(text)
#         return round(tokens * self.MODEL_COSTS[model], 5)

#     def get_combination_options(self, query, model_list):
#         decomposed_queries = self.decompose_query(query)

#         # Currently not using model_list, need to add that in! 
#         # CURRENTLY FAILS IF ONLY ONE PROMPT, NEED TO CHANGE THAT! 

#         if len(decomposed_queries) == 1: 
#             costs = [
#                 {
#                     "combo" : [(model1, decomposed_queries[0])],
#                     "cost": self.calculate_cost(decomposed_queries[0], model1),
#                 }
#                 for model1 in self.MODEL_COSTS
#             ]

#         elif len(decomposed_queries) == 2: 
#             costs = [
#                 {
#                     "combo" : [(model1, decomposed_queries[0]), (model2 , decomposed_queries[1])],
#                     "cost": self.calculate_cost(decomposed_queries[0], model1) + self.calculate_cost(decomposed_queries[1], model2),
#                 }
#                 for model1 in self.MODEL_COSTS
#                 for model2 in self.MODEL_COSTS
#             ]
#         else: 
#             raise NotImplementedError

#         costs.sort(key=lambda x: x["cost"])
#         return costs

    
