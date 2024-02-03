# J-WATR BUFFALO - An Enterprise LLM Gateway 🐃
***Boundless User-Focused Framework for Advanced LLM Optimzation*** 

&nbsp; &nbsp;

> **tl;dr** - Cisco Research proudly presents BUFFALO, a **flexible**, **open-source** enterprise **gateway** for _LLMs_.
> 
> Check out our [TechBlog](https://techblog.cisco.com/), [Slide Deck](/Buffalo_Slides.pdf), [Demo Input](/BUFFALO_2min_InputLayer.mp4), and [Demo Output](/BUFFALO_2min_OutputLayer.mp4) for more information and exciting applications!
> 
> Make sure to use the **Table of Contents** (the three horizontal lines next to `README.md`) for easier viewing!

&nbsp; &nbsp;

## Why BUFFALO? 

The guiding question in our creation of BUFFALO was simple: 
> ***"Why can't an enterprise deploy GPT-4, LLAMA-2, or any other LLM for both internal and external usage?"***

Our team identified several limitations of the LLM landscape which prevent Enterprises from readily deploying LLM-based solutions. 

|                                                 |                                                 |                                                |                                             |                                           |                                                  |
|:-----------------------------------------------:|-------------------------------------------------|------------------------------------------------|---------------------------------------------|-------------------------------------------|--------------------------------------------------|
|                 **Data Privacy**                |                   **Expenses**                  |                **Data Security**               |              **Hallucinations**             |             **Explainability**            |                  **Competence**                  |
| Sharing PII, divulging customer/enterprise data | Cost/power, usage limitation, redundant queries | Leaking confidential data, unauthorized access | Misleading information, improper tool usage | Robustness, removal of bias, truthfulness | Lack of reasoning, attribution, false confidence |

&nbsp; &nbsp;

#### Installing Python Packages 

To start, we can clone this repository using: 
```
git clone https://github.com/cisco-open/Buffalo.git
```

Next, we must install the necessary packages for BUFFALO. For this, we have two options:

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

&nbsp; &nbsp;

#### Installing Elasticsearch 

Elasticsearch needs to be running in the background for the Output Verification component. 
Please download Elasticsearch 8.9.0 at the following link [Elasticsearch Download](https://www.elastic.co/downloads/elasticsearch)

Next, ensure that security settings are disabled by going to `Elasticsearch.yml` in the Elasticsearch installation folder and setting the following: 

```
xpack.security.enabled: false
xpack.security.enrollment.enabled: false
```
[More Info - Disabling Elasticsearch Security](https://discuss.elastic.co/t/disable-authentification-for-elasticsearch/304862/3)

&nbsp; &nbsp;

#### Installing Stanford CoreNLP 

> ***JAVA needs to be installed to run OpenIE!***

Stanford CoreNLP also needs to be installed in order to run the Ouput Verification component. 
The zip folder can be downloaded from [Stanford OpenIE Repo](https://stanfordnlp.github.io/CoreNLP/download.html)

&nbsp; &nbsp;

#### Installing RANNET Model 

Both RANNET base english model and model-store need to be downloaded. These can be found on the RANNET GitHub page. 

&nbsp; &nbsp;

## Usage (Demos) 

Having completed installation, launching BUFFALO is as easy as 1, 2, 3. 

#### Step 1) Launching Elasticsearch 

You can launch Elasticsearch by navigating to the downloaded, unzipped directory, and using the corresponding command.

[More Info - Launching ElasticSearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/starting-elasticsearch.htmls)

```
.\bin\elasticsearch.bat
```

&nbsp; &nbsp;

#### Step 2) Starting up the REST API Server

Next, navigate to the gateway folder and start the backend 

```
cd gateway
python app.py 
```

&nbsp; &nbsp;

#### Step 3) Starting the Streamlit Frontend

Wait for a few seconds to ensure the server is up and running. 

Next, launch streamlit by going back to the top-level directory: 

```
cd ..
streamlit run main.py
```

And voila! A link should pop up taking us to our dashboard gateway. 

&nbsp; &nbsp;

## Architecture 

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

## Contributing & Future Directions

> We have several TODO's spread out throughout our files! We will continue working in these directions to improve BUFFALO, adjusting as needed based on our user's feedback

Currently, we are working on implementing the following features, split by component-of-focus: 

|                    |                                                                                                                                                                                                                                                                                                                                                                                                                    |
|:------------------:|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     **Overall**    | <ul><li>Some way to store session state so can have chat history</li><li>Json dictionary from end-to-end (need to discuss some new ideas)</li><li>Model Comparison (benchmark of prompts to multiple models, give truthfulness score)</li><li>Can sample a few datapoints to run check against (show comparison on how they work)</li><li>Running multiple models (can ask Vamsi)</li><li>Using GPT4 to tag (connecting prompt and verification)</li></ul>  |
| **Model-Specific** | <ul><li>Change model so we're loading from huggingface + have a dedicated class</li></ul>                                                                                                                                                                                                                                                                                                                                          |
|  **Prompt Layer**  | <ul><li>Say cost options can be configured by admin (verbosity), add to admin.yml</li></ul>                                                                                                                                                                                                                                                                                                                                        |
|    **LLM Cache**   | <ul><li>Someway to give cache more than one document</li><li>If cache partial hit, need option to ONLY query LLM w/ non-cache hit (some way to specify for each)</li><li>If cache hit, but still LLM, and LLM score better, replace cache entry w/ better result or append</li></ul>                                                                                                                                                          |
|  **Exfiltration**  | <ul><li>Remove squad documents (or be able to toggle off)</li><li>Need to not only add file names, but also big ideas (ex. "Financial Information About Cisco")</li><li>Solidify Idea Embeddings research ^^</li></ul>                                                                                                                                                                                                                       |
|  **Verification**  | <ul><li>Need to separate between retrieval augmented correction/generation</li><li>Will NOT send docs to LLM until we explicitly ask it to</li></ul>                                                                                                                                                                                                                                                                                   |
|  **Miscellaneous** | <ul><li>Create + Test Conda Env</li><li>Merge Elasticsearch launch into backend start</li></ul>                                                                                                                                                                                                                                                                                                                                           |

If you wish to contribute or suggest any additional funtionalities, please check out [Contributing Guidelines](/CONTRIBUTING.md)

## Acknowledgements  

BUFFALO would not have been possible without the contributions of the following individuals, to whom we express our gratitude: 

- **Jayanth Srinivasa**, **Advit Deepak**, **Will Healy**, **Raunak Sinha**, **Tarun Raheja**, Goli Vamsi Krishna Mohan, Ramana Kompella, Vijoy Pandey
- The entirety of the Cisco Research team for their feedback, ideas, and support 🥳

Thank you so much for checking us out! 🐃

&nbsp; &nbsp;

