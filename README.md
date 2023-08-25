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

Need to pip install the following (and more): 

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

Raunak's RANNET has already been included in the folder, and should be ready to go. It's the reason why this repo is 600 MB+ lol 

> JUST KIDDING, THE ABOVE STATEMENT IS ONLY TRUE FOR THE .ZIP FILE VERSION, NOT FOR THE GITHUB VERSION. FOR THE GITHUB VERSION, BOTH OF THOSE NEED TO BE INSTALLED. BOTH OF THOSE FOLDERS (there are two RANNET folders) have been ZIPPED AND SENT IN THE WEBEX CHAT. UNZIP IT INTO THE MODELS FOLDER, AND YOU SHOULD BE GOOD TO GO!!

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
streamlit main.py
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

**Input Layer Methods**
- (POST) /prompt/post = recieves input prompt and selected models, returns cost options 
- (POST) /cache/post = receives prompt, returns cache results (***THIS IS ALSO USED FOR LLM QUERYING ATM***)

> Essentially, when cache threshold is set to a really high value, it queries the LLM --> so we're using the above endpoint for 2 different things 
> This needs to be changed to allow for models beyond GPT3.5, which will be done soon 

**Output Layer Methods** 
- (POST) /exfiltrator/post = receives output of llm, returns leaks, if any 
- (POST) /verify/facts/post = receives LLM output, returns facts, if any
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
- NEED TO ENSURE THAT YML FILE GOES TO ALL MODULES 
- MAKE IT CONFIGURABLE USING YML FILE 
- Some way to store session state so can have chat history 
- Json dictionary from end-to-end (need to discuss some new ideas)
- Model Comparison (benchmark of prompts to multiple models, give truthfulness score)
  - Can sample a few datapoints to run check against (show comparison on how they work)
  - Running multiple models (can ask Vamsi)
- Using GPT4 to tag (connecting prompt and verification)

**Model-Separation**
- Change model so we're loading from huggingface + have a dedicated class
  - It's calculation specific too atm! 
- issue w/ cache gpt usage is that cant actually be an LLM


**Prompt-Layer**
- Update prompt layer so it works w/ any len of decomposed queries 
- Make it scalable via for loop instead of if statements
- Say cost options can be configured by admin 

**Cache-Layer**
- someway to give cache more than one document 
- Remove the cache implementation where we're calling gpt from there 
- If cache partial hit, need option to ONLY query LLM w/ non-cache hit (some way to specify for each)

**Exfiltration****
  - Remove squad documents, point to docs in ./docs
  - Figure out what's wrong w/ Data Exfiltration leak detection 
  - Need to do the verification check in reverse! (so once LLM, before showing results, run LLM check)


**Verification** 
- Update so slider in doc id actually matters
- Update so prompt/response topics are correct  
- Need to separate between retrieval augmented correction/generation
  - Will NOT send docs to LLM until we explicitly ask it to


**Miscellaneous**
- Need to create readme
  - Create conda env yml for easy installation 
