pip install requests pandas

import requests
import pandas as pd

# Configurações
dynamics_url = "https://<seu-instance>.crm.dynamics.com/api/data/v9.0/"
client_id = "<seu-client-id>"
client_secret = "<seu-client-secret>"
tenant_id = "<seu-tenant-id>"
resource = "https://<seu-instance>.crm.dynamics.com"
auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"

# Dados processados (Exemplo em DataFrame)
data = [
    {"id": "12345", "name": "John Doe", "email": "john.doe@example.com"},
    {"id": "67890", "name": "Jane Smith", "email": "jane.smith@example.com"}
]
df = pd.DataFrame(data)

# Função para obter o token de acesso
def get_access_token():
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "resource": resource,
        "grant_type": "client_credentials"
    }
    response = requests.post(auth_url, data=payload)
    response.raise_for_status()
    return response.json()["access_token"]

# Função para enviar os dados ao Dynamics 365
def send_data_to_dynamics(df):
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    for index, row in df.iterrows():
        record_id = row["id"]
        data = {
            "fullname": row["name"],
            "emailaddress1": row["email"]
        }

        # Tenta atualizar o registro se existir, ou cria um novo se não existir
        response = requests.patch(
            url=f"{dynamics_url}contacts({record_id})",
            headers=headers,
            json=data
        )
        
        if response.status_code == 404:  # Registro não encontrado, cria um novo
            response = requests.post(
                url=f"{dynamics_url}contacts",
                headers=headers,
                json=data
            )

        # Log do status
        if response.status_code in [200, 204]:
            print(f"Registro atualizado/criado: {record_id}")
        else:
            print(f"Erro ao processar registro {record_id}: {response.text}")

# Enviar os dados
send_data_to_dynamics(df)

