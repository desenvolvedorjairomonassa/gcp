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

