# projeto-dynamics365
Projeto de uso da API do Dynamics 365

# Dynamics 365 Data Sync Script

Este repositório contém um script em Python para enviar dados processados de volta ao Microsoft Dynamics 365 utilizando a API REST. O script permite criar ou atualizar registros na entidade especificada no Dynamics 365.

---

## 🚀 Funcionalidades

- **Autenticação**: Geração de token OAuth 2.0 para autenticação com o Azure AD.
- **Envio de Dados**: Atualiza registros existentes ou cria novos, caso o registro não exista.
- **Log Simples**: Exibe no terminal o status de cada operação (atualização/criação ou erro).

---

## 📋 Pré-requisitos

1. **Conta do Dynamics 365** com permissões para acessar a API REST.
2. **Azure Active Directory App Registration**:
   - Registre uma aplicação no portal do Azure para obter o `Client ID`, `Client Secret` e `Tenant ID`.
   - Dê permissões à aplicação para acessar o Dynamics 365 como API.

3. **Python 3.8+** com as bibliotecas:
   - `requests`
   - `pandas`

Instale as dependências com:
```bash```
```pip install requests pandas```

## 🚀 Configuração
1. Atualize as Configurações do Script
Edite as seguintes variáveis no arquivo principal (dynamics_sync.py):

# Configurações da API Dynamics 365
```dynamics_url = "https://<seu-instance>.crm.dynamics.com/api/data/v9.0/"```
```client_id = "<seu-client-id>"```
```client_secret = "<seu-client-secret>"```
```tenant_id = "<seu-tenant-id>"```
```resource = "https://<seu-instance>.crm.dynamics.com"```

## 📋 Estrutura dos Dados
Certifique-se de que os dados processados estão em um formato compatível (exemplo: um DataFrame do pandas) com as colunas necessárias.

Prepare seus Dados: Garanta que os dados que você deseja enviar estejam em um arquivo CSV ou diretamente em um DataFrame.

Execute o Script: Execute o script principal para processar os dados e enviá-los ao Dynamics 365:

```python dynamics_sync.py```

# Segurança
Nunca compartilhe seu Client Secret publicamente.
Use variáveis de ambiente para armazenar informações sensíveis. Exemplo

```import os```
```client_secret = os.getenv("DYNAMICS_CLIENT_SECRET")```

# Estrutura do Repositório
.
├── dynamics_sync.py      # Script principal
├── requirements.txt      # Dependências do projeto
├── example_data.csv      # Dados de exemplo para teste
└── README.md             # Documentação do projeto

# Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

# Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests. Para mudanças maiores, por favor, abra uma discussão primeiro.

# Instruções de Deploy
Deploy Local
Clone o repositório:

```git clone https://github.com/seu-usuario/dynamics365-sync.git```
```cd dynamics365-sync```

# Crie um ambiente virtual (opcional, mas recomendado):
```python -m venv venv```
```source venv/bin/activate  # No Windows: venv\Scripts\activate```

# Instale as dependências:
```pip install -r requirements.txt```

Contato
Criado por Demetrius Mata
Entre em contato para dúvidas ou suporte: dmdataconsultoria@gmail.com

