import pandas as pd
import pyodbc

# Configurações de conexão para o banco de dados no Azure
server = "seu-servidor.database.windows.net"
database = "seu-banco-de-dados"
username = "seu-usuario"
password = "sua-senha"
driver = "{ODBC Driver 17 for SQL Server}"

# Conectando ao banco
connection_string = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}"
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Criando a tabela no banco de dados
create_table_query = """
CREATE TABLE FakeDataset (
    id INT PRIMARY KEY,
    name NVARCHAR(255),
    email NVARCHAR(255),
    address NVARCHAR(MAX),
    phone_number NVARCHAR(50),
    date_of_birth DATE,
    created_at DATETIME
);
"""
try:
    cursor.execute(create_table_query)
    conn.commit()
    print("Tabela criada com sucesso!")
except Exception as e:
    print("Erro ao criar tabela:", e)

# Carregando os dados do CSV
df = pd.read_csv("fake_dataset.csv")

# Inserindo os dados no banco de dados
for _, row in df.iterrows():
    insert_query = """
    INSERT INTO FakeDataset (id, name, email, address, phone_number, date_of_birth, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(insert_query, row.id, row.name, row.email, row.address, row.phone_number, row.date_of_birth, row.created_at)
    conn.commit()

print("Dados inseridos com sucesso!")
conn.close()
