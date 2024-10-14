## Overview do desafio 
Extração de dados de PDFs com Gemini e inserção em AlloyDB

Este repositório demonstra como criar uma Cloud Function para processar PDFs, utilizando o Gemini para extrair informações relevantes (como data do contrato e número do processo) e armazená-las no AlloyDB.

### Configuração Inicial
1. **Criar um projeto no Google Cloud**:
   - Acesse o Google Cloud Console e crie um novo projeto.

2. **Ativar as APIs necessárias**:
   - Ative as APIs do Google Cloud Storage, Cloud Functions, e qualquer outra API necessária para a integração com o Gemini e AlloyDB.
   - ** Importante: indicar vpc na Cloud storage para acessar serviços da GCP
   - criar service account para Cloud Storage para acessar recursos Alloydb e a pasta especifica do cloud storage e Gimini

3. **Configurar o serviço Google Cloud Storage**:
   - Crie um bucket no Google Cloud Storage para armazenar os arquivos PDF.

4. **Configurar gatilhos**:
   - Configure um gatilho que será acionado quando um novo arquivo PDF for adicionado ao bucket do Google Cloud Storage.

### Considerações Finais
- **Monitoramento e Logs**:
  - Utilize o Google Cloud Monitoring e Logging para acompanhar a execução da função e solucionar problemas.
- **Gerenciamento de Custos**:
  - Monitore os custos associados à execução da função e ao uso das APIs para evitar surpresas na fatura.
- **Atualizações e Manutenção**:
  - Mantenha a função atualizada com as melhores práticas e atualizações das APIs utilizadas.

## Melhorias
Refactorar o serviço monolítico em microserviços usando
- Uma cloud Function para extrair informações
- pubsub para receber os novos arquivos para extrair
- pubsub para receber os dados extraidos
- cloud function para pegar do pubsub e inserir no Alloydb
