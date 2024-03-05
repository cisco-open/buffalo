---
sidebar_position: 4
---

# Architecture

Let's take a quick look at how our BUFFALO gateway works under the hood. 

The backend (gateway) is a REST API server which we started by running `python app.py`

This server contains ALL the actual gateway components/computations, allowing the streamlit frontend to be as light as possible. 

All streamlit does is call the REST API server w/ corresponding GET/POST request, and displays the output. 

All REST API endpoints can be seen in `app.py`, and they are summarized here: 

|                  |                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|:----------------:|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|    **General**   | <ul><li>(GET) / = default, ensures server is up</li><li>(GET) /reset = resets server state</li><li>(GET) /docs = gets all documents and file sizes in Enterprise Knowledge Base (set to the .\gateway\docs folder)</li><li>(GET) /model_list = gets list of all models as specified in admin.yml</li><li>(POST) /model = receives query, returns answer given specific LLM</li></ul>                                                                                               |
|  **Input Layer** | <ul><li>(POST) /prompt/post = recieves input prompt and selected models, returns cost options</li><li>(POST) /cache/search/post = receives prompt, returns cache results</li><li>(POST) /cache/model/post = receives query, returns document-specific LLM response (if applicable)</li><li>(POST) /cache/add/post = receives prompt/query, adds to cache</li></ul>                                                                                                          |
| **Output Layer** | <ul><li>(POST) /exfiltrator/post = receives output of llm, returns leaks, if any</li><li>(POST) /exfiltrator/topic/post = receives output of llm, returns list of relevant topics/facts</li><li>(POST) /verify/facts/post = receives LLM output, returns list of facts</li><li>(POST) /verify/ie/post = receives list of facts, retruns relation triplets for each, if any</li><li>(POST) /verify/triplet/post = receives list of triplets, returns matches/info if found</li></ul> |


New endpoints can be added in a similar format to app.py 

These endpoints simply call the corresponding functions from each of the classes. The four files house all of the classes/methods for each of the four components (`prompt.py` : QueryProcessor, `cache.py` : QACache, `leaks.py` : ExfiltrationModel, `verify.py` : VerificationModel). 

And in Streamlit, our frontend is split into three parts: Col1, Col2A, Col2B
- Col1 is on the left hand side, where the user enters prompt and can see what documents are in the Knowledge base 
- Col2A is on the right hand side, and displayed first which shows the Prompt and Cache 
- Col2B is shown after "Submit to LLM" is selected in Col2A, and it shows the Exfiltration and Verification components

&nbsp; &nbsp;