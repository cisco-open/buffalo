---
sidebar_position: 3
---

# Usage (Demos) 

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
