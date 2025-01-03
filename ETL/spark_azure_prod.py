from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year
import os

# Definição do ambiente: "dev", "homolog", "prod"
env = "prd"  # Altere para "homolog" ou "prod" conforme necessário

# Configurações específicas para cada ambiente
config = {
    "prod": {
        "app_name": "DataProcessingProd",
        "adls_container": "prod-container",
        "adls_account": "seu_adls_account_name",
        "adls_key": "sua_adls_access_key",
        "input_path": "fake_dataset_prod.csv",
        "output_path": "prod/processed_data"
    }
}

# Seleciona as configurações do ambiente atual
current_config = config[env]

# Configuração para acessar o Azure Data Lake
os.environ["fs.azure.account.key.{}.dfs.core.windows.net".format(current_config["adls_account"])] = current_config["adls_key"]

# Inicializando Spark
spark = SparkSession.builder \
    .appName(current_config["app_name"]) \
    .config("fs.azure.account.key.{}.dfs.core.windows.net".format(current_config["adls_account"]), current_config["adls_key"]) \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Caminho completo do Data Lake (input e output)
adls_input_path = f"abfss://{current_config['adls_container']}@{current_config['adls_account']}.dfs.core.windows.net/{current_config['input_path']}"
adls_output_path = f"abfss://{current_config['adls_container']}@{current_config['adls_account']}.dfs.core.windows.net/{current_config['output_path']}"

# Carregar o dataset do Data Lake
df = spark.read.csv(adls_input_path, header=True, inferSchema=True)

# Processamento de dados: Adicionar coluna com a idade
processed_df = df.withColumn("age", year("created_at") - year("date_of_birth"))

# Exibir amostra do processamento
processed_df.show(10)

# Salvar os dados processados em Delta Table
processed_df.write.format("delta").mode("overwrite").save(adls_output_path)

print(f"Dados processados e salvos no Azure Data Lake no caminho: {adls_output_path}")
spark.stop()
