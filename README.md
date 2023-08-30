# Enterprise LLM Gateway 

> This is a very, very rough README. Please reach out if you have any questions! 

&nbsp; &nbsp;


## Required Things: 

### Installing Elasticsearch 

Elasticsearch (needs to be running in the background)
Please download Elasticsearch at the followign link [Elasticsearch Download](https://www.elastic.co/downloads/elasticsearch)

&nbsp; &nbsp;

### Installing Stanford CoreNLP 

> **JAVA needs to be installed to run OpenIE!**

Stanford CoreNLP (need to have Java installed for this)
The zip folder can be downloaded from [Stanford OpenIE Repo](https://stanfordnlp.github.io/CoreNLP/download.html)

&nbsp; &nbsp;

### Installing Python Packages 

> Will have a conda env/requirements.txt coming soon! 

Need to pip install the following: 

- streamlit 
- annotated_text
- faiss 
- langchain 
- rannet 
- nltk 
- openie 
- elasticsearch 
- spacy 

There will be a few models downloaded as well, including: 
- lighteternal/fact-or-opinion-xmlr-el 

### Installing RANNET 

> TODO: Docker image will take care of this -- coming soon! 

Both RANNET base english model and model-store need to be downloaded. These can be found on the RANNET GitHub page. 

&nbsp; &nbsp;


## Actually Running: 

### 01) Kicking off Elasticsearch

First, ensure that Elasticsearch is running in the background. 

Ensure that security settings are disabled by going to `Elasticsearch.yml` in the Elasticsearch installation folder and setting the following: 

```

xpack.security.enabled: false
xpack.security.enrollment.enabled: false
```

[More Info - Disabling Elasticsearch Security](https://discuss.elastic.co/t/disable-authentification-for-elasticsearch/304862/3)



You can launch Elasticsearch by navigating to the downloaded, unzipped directory, and using the corresponding command.

[More Info - Launching ElasticSearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/starting-elasticsearch.htmls)

```
.\bin\elasticsearch.bat
```

&nbsp; &nbsp;


### 02) Launching the REST API Server

Next, navigate to the gateway folder and start the backend 

```
cd gateway
python app.py 
```

&nbsp; &nbsp;


### 03) Starting the Streamlit Frontend 

Wait for a few seconds to ensure the server is up and running. 

Next, launch streamlit by going back to the top-level directory: 

```
cd ..
streamlit run main.py
```

&nbsp; &nbsp;

## How it All Works 

So, the backend is a REST API server which you start up by running python app.py. 

This server contains ALL the actual gateway components/computations, allowing the streamlit frontend to be as light as possible. 

All streamlit does is call the REST API server w/ corresponding GET/POST request, and displays the output. 

All REST API endpoints can be seen in app.py, and they are summarized here: 

**General Methods**
- (GET) / = default, ensures server is up 
- (GET) /reset = resets server state 
- (GET) /docs = gets all documents and file sizes in Enterprise Knowledge Base (set to the .\gateway\docs folder)
- (GET) /model_list = gets list of all models as specified in admin.yml
- (POST) /model = receives query, returns answer given specific LLM 

**Input Layer Methods**
- (POST) /prompt/post = recieves input prompt and selected models, returns cost options 
- (POST) /cache/search/post = receives prompt, returns cache results 
- (POST) /cache/model/post = receives query, returns document-specific LLM response (if applicable) 
  (POST) /cache/add/post = receives prompt/query, adds to cache 

**Output Layer Methods** 
- (POST) /exfiltrator/post = receives output of llm, returns leaks, if any
- (POST) /exfiltrator/topic/post = receives output of llm, returns list of relevant topics/facts
- (POST) /verify/facts/post = receives LLM output, returns list of facts
- (POST) /verify/ie/post = receives list of facts, retruns relation triplets for each, if any 
- (POST) /verify/triplet/post = receives list of triplets, returns matches/info if found 

New endpoints can be added in a similar format to app.py 

These endpoints simply call the corresponding functions from each of the classes. 

The four files house all of the classes/methods for each of the four components: 
- prompt.py --> QueryProcessor
- cache.py --> QACache
- leaks.py --> ExfiltrationModel
- verify.py --> VerificationModel 

And in Streamlit, our frontend is split into three parts: Col1, Col2A, Col2B
- Col1 is on the left hand side, where the user enters prompt and can see what documents are in the Knowledge base 
- Col2A is on the right hand side, and displayed first which shows the Prompt and Cache 
- Col2B is shown after "Submit to LLM" is selected in Col2A, and it shows the Exfiltration/Verification

&nbsp; &nbsp;

## Works-In-Progress: 

**Overall**
- Some way to store session state so can have chat history 
- Json dictionary from end-to-end (need to discuss some new ideas)
- Model Comparison (benchmark of prompts to multiple models, give truthfulness score)
  - Can sample a few datapoints to run check against (show comparison on how they work)
  - Running multiple models (can ask Vamsi)
- Using GPT4 to tag (connecting prompt and verification)

**Model-Separation**
- Change model so we're loading from huggingface + have a dedicated class

**Prompt-Layer**
- Say cost options can be configured by admin (verbosity)

**Cache-Layer**
- someway to give cache more than one document 
- If cache partial hit, need option to ONLY query LLM w/ non-cache hit (some way to specify for each)
- If cache hit, but still LLM, and LLM score better, replace cache entry w/ better result or append

**Exfiltration****
  - Remove squad documents (or be able to toggle off)
  - Need to not only add file names, but also big ideas (ex. "Financial Information About Cisco") 

**Verification** 
- Need to separate between retrieval augmented correction/generation
  - Will NOT send docs to LLM until we explicitly ask it to


**Miscellaneous**
- Need to create readme
  - Create conda env yml for easy installation
  - Finish docker image 
