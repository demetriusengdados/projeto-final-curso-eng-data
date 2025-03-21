'''Integração direta com Dynamics 365 API
Extração dos Dados:

Use a API REST do Dynamics 365 para extrair os dados. 
A API fornece endpoints para acessar entidades específicas.
Utilize um notebook ou script em Python que consuma a API REST, salve os dados em arquivos CSV/JSON no Data Lake da Azure.'''

import requests
import json
from azure.storage.blob import BlobServiceClient

# Configurações
dynamics_url = "https://<seu-instance>.crm.dynamics.com/api/data/v9.0/contacts"
headers = {
    "Authorization": "Bearer <access_token>",
    "Accept": "application/json"
}
azure_connection_string = "<azure_connection_string>"
container_name = "data-lake"

# Extração dos dados
response = requests.get(dynamics_url, headers=headers)
data = response.json()

# Salvando os dados no Data Lake
blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
blob_client = blob_service_client.get_blob_client(container=container_name, blob="contacts.json")
blob_client.upload_blob(json.dumps(data), overwrite=True)
