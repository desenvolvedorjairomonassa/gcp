import os
import json
import PyPDF2
import psycopg2
from google.cloud import secretmanager
from google.cloud import storage
from google.cloud import functions_v1
from google.cloud import aiplatform
import google.generativeai as genai

def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{os.getenv('GCP_PROJECT')}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def extract_text_from_pdf(file_path, start_page, end_page):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        for page_num in range(start_page, end_page):
            page = reader.getPage(page_num)
            text += page.extract_text()
    return text

def extract_entities_with_gimini(text, gimini_key, gimini_url):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Create the model
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 8192,
      "response_mime_type": "application/json",
    }
    safety_settings = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
        )
    ]
    model = genai.GenerativeModel(
      model_name="gemini-1.5-pro",
      generation_config=generation_config,
      safety_settings=safety_settings,
      system_instruction="""você é um agente que vai extrair informações e entidades dos processos em pdf: extraia :  
          Nome completo\nCPF/CNPJ, Tipo de parte (autor, réu, terceiro), Endereço, Advogados: Nome completo, OAB, Juiz: Nome completo, 
          Varas/Tribunais:\nNome da vara/tribunal, Comarca, Datas: Data de distribuição, Data da última movimentação, Datas de audiências, 
          Data da sentença\nValores: Valor da causa Assuntos: Assunto principal""",
    )
    
    chat_session = model.start_chat(
      history=[
        {
          "role": "user",
          "parts": [
            files[0],
          ],
        },
      ]
    )
    
    response = chat_session.send_message("extraia")  
    return response.json()

def insert_into_alloydb(data, db_config):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    query = """
    INSERT INTO processos_juridicos (data_contrato, numero_processo)
    VALUES (%s, %s)
    """
    cursor.execute(query, (data['data_contrato'], data['numero_processo']))
    conn.commit()
    cursor.close()
    conn.close()

@functions_framework.event
def main(event, context):
    # Obter chaves e configurações do Secret Manager
    gimini_key = get_secret("gimini_key")
    gimini_url = get_secret("gimini_url")
    db_config = json.loads(get_secret("alloydb_config"))

    # Obter o arquivo do Cloud Storage
    bucket_name = event['bucket']
    file_name = event['name']
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    local_file_path = f"/tmp/{file_name}"
    blob.download_to_filename(local_file_path)

    # Extrair texto das primeiras 15 páginas do PDF
    text = extract_text_from_pdf(local_file_path, 0, 15)

    # Extrair entidades usando Gimini
    entities = extract_entities_with_gimini(text, gimini_key, gimini_url)

    # Inserir dados no AlloyDB
    insert_into_alloydb(entities, db_config)

    print("Processamento concluído com sucesso.")
