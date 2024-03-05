---
sidebar_position: 2
---

# Installation

#### Installing Python Packages 

To start, we can clone this repository using: 
```
git clone https://github.com/cisco-open/BUFFALO.git
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
