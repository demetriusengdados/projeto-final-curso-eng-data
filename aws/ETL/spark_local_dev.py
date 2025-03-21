from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year

# Configurações de Spark para diferentes ambientes
env = "dev"  # Alterar para "homolog" ou "prod" conforme o ambiente

config = {
    "dev": {
        "app_name": "DataProcessingDev",
        "master": "local[*]",
        "path": "fake_dataset.csv"
    },
    "homolog": {
        "app_name": "DataProcessingHomolog",
        "master": "local[*]",
        "path": "fake_dataset.csv"
    },
    "prod": {
        "app_name": "DataProcessingProd",
        "master": "yarn",  # Alterar conforme a configuração do cluster de produção
        "path": "fake_dataset.csv"
    }
}

# Inicializando Spark
spark = SparkSession.builder \
    .appName(config[env]["app_name"]) \
    .master(config[env]["master"]) \
    .getOrCreate()

# Carregar o dataset
df = spark.read.csv(config[env]["path"], header=True, inferSchema=True)

# Processamento de dados: Adicionar coluna com a idade
processed_df = df.withColumn("age", year("created_at") - year("date_of_birth"))

# Exibir amostra do processamento
processed_df.show(10)

# Salvar resultados processados em Delta Table (simulação de ambiente real)
output_path = f"processed_data_{env}"
processed_df.write.format("delta").mode("overwrite").save(output_path)

print(f"Dados processados salvos no caminho: {output_path}")
spark.stop()
