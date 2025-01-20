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

# Job Dataflow template

A Dataflow template in Google Cloud Platform (GCP) is a pre-packaged Dataflow pipeline that can be easily deployed. These templates allow you to separate pipeline design from deployment, making it easier for different team members to collaborate. You can use templates to automate and streamline data processing tasks without needing a development environment1.
link <a href="https://cloud.google.com/dataflow/docs/concepts/dataflow-templates">Dataflow template </a>

<img src="Captura de tela 2024-09-25 213615.png">

# Required Parameters from dataflow job
<img src="Captura de tela 2024-09-25 213830.png">


# Service account
A service account in Google Cloud Platform (GCP) is a special type of account used by applications or virtual machines, or dataflow jobs to interact with GCP services, rather than by individual users

The principle of least privilege means granting only the minimum permissions necessary for a user or service to perform its tasks, reducing the risk of unauthorized access: In this case you have to give this roles for service account running the job: bigquery data editor, bigquery job user, dataflow worker, storage object user
<img src="Captura de tela 2024-09-25 213845.png">

# Runned : Succeeded
<img src="Captura de tela 2024-09-25 213949.png">

# Predict using SQL command
ML.FORECAST(MODEL ‘dataset.model_name)
<img src="Captura de tela 2025-01-19 222827.png">

# Exploring with BI (looker studio)
<img src="Captura de tela 2025-01-19 222901.png">

# Time Series Graph 
<img src="Captura de tela 2025-01-19 222933.png">

# using notebook 
<img src="Captura de tela 2025-01-19 223016.png">

 # using notebook with pandas
<img src="Captura de tela 2025-01-19 223024.png">

# Another data ingestion
<img src="Captura de tela 2025-01-19 223032.png">

# using visual interface
<img src="Captura de tela 2025-01-19 223038.png">
