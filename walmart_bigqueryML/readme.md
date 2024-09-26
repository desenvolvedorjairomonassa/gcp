## Building Data Pipelines for Machine Learning with BigQuery - gcp
The goal is to transfer the dataset to BigQuery and utilize BigQueryML to demonstrate how easy it is to create prediction models using SQL.

# Steps:
<img src="Captura de tela 2024-05-10 133354.png" alt="Descrição da imagem">

- **Load the data from Kagle to Cloud storage**.
- **Using dataflow template in order to migrate the data**.
- **Copy data to BigQuery**.
- **Create dataset**.
- **Create Model**.
- **Evaluation**.
- **Batch predictions**.

# ingestion
The source data is from Kaggle, specifically Walmart sales. You can either download it directly from Kaggle or access it through this repository. I uploaded the data to Cloud Storage and then utilized Dataflow with a template to load the CSV files into BigQuery
source: https://www.kaggle.com/datasets/mikhail1681/walmart-sales/data


# Bigquery, benefits:
<img src="Captura de tela 2024-05-10 133527.png" alt="Descrição da imagem">

- **Scalability**
- Serverless
- High Performance
- Petabyte Analysis in Seconds
- Columnar Storage
- Integrated Machine Learning
- High Availability
- Security

# Cloud Dataflow:
<img src="Captura de tela 2024-05-10 133549.png" alt="Descrição da imagem">


- Batch or streaming processing
- Serveless
- Various integrations
- Can be coded in Python or Java

# Cloud Bigquery ML
<img src="Captura de tela 2024-05-10 133608.png" alt="Descrição da imagem">

- Facilita acesso ao ML
- Usa linguagem SQL
- Aumenta velocidade inovação
- Integra outras ferramentas do GCP

# hands-on 
Architecture 
<img src="Captura de tela 2024-05-10 133633.png">

- File available in cloud storage
- Move forward using dataflow from cloud storage to bigquery

# you need 

- Dataset Kaggle www.kaggle.com
- Walmart Sales (kaggle.com)
- https://console.cloud.google.com/ FreeTier 300 dollars
  
# create new project
<img src="Captura de tela 2024-09-25 155516.png">

# Enter the name you want
<img src="Captura de tela 2024-09-25 155814.png">

# create new bucket
<img src="Captura de tela 2024-09-25 155913.png">

# Get the dataset
- Download the dataset from Kaggle.
- Take a look at the CSV file.
- Create a schema for the CSV in JSON format.
- Upload the dataset to the newly created bucket.(or get the git file walmart_sales.csv)
- Upload the schema to the bucket. (see schema-walmart.json)

# create dataset in Bigquery and then create a table in this dataset
<img src="Captura de tela 2024-09-25 160226.png">

<img src="Captura de tela 2024-09-25 161737.png">


# enable api dataflow via cli
in CLI type "gcloud services enable dataflow.googleapis.com"



