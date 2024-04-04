Para utilizar python no SDK do vertex
- Install Vertex AI SDK:

  !pip install google-cloud-aiplatform protobuf==3.19.3 --upgrade --user <br>
  !pip install -U google-cloud-aiplatform "shapely<2"

- Authenticating

  "import vertexai

  PROJECT_ID = "project_name"  
  REGION = "us-central1"  

  vertexai.init(project=PROJECT_ID, location=REGION)"

- chamar as bibliotecas:

  "from vertexai.language_models import TextGenerationModel
   from vertexai.language_models import ChatModel"

- carregar o modelo :

  "generation_model = TextGenerationModel.from_pretrained("text-bison@001")"

- finalmente, usar o prompt :
 "
  prompt = "Quais são os elementos químicos derivados do petróleo"

  print(generation_model.predict(prompt=prompt, max_output_tokens=256).text)

  "
