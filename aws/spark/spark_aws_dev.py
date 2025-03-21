from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year
import os

# Definição do ambiente: "dev", "homolog", "prod"
env = "dev"  # Altere para "homolog" ou "prod" conforme necessário

# Configurações específicas para cada ambiente
config = {
    "dev": {
        "app_name": "DataProcessingDev",
        "s3_bucket": "dev-bucket",  # Nome do bucket no S3 para DEV
        "s3_key": "seu_aws_access_key",
        "s3_secret": "sua_aws_secret_key",  # Utilize AWS Secrets Manager em produção
        "input_path": "fake_dataset_dev.csv",  # Caminho no S3 para os dados
        "output_path": "dev/processed_data"
    },
}

# Seleciona as configurações do ambiente atual
current_config = config[env]

# Configuração para acessar o Amazon S3
os.environ["AWS_ACCESS_KEY_ID"] = current_config["s3_key"]
os.environ["AWS_SECRET_ACCESS_KEY"] = current_config["s3_secret"]

# Inicializando Spark
spark = SparkSession.builder \
    .appName(current_config["app_name"]) \
    .config("spark.hadoop.fs.s3a.access.key", current_config["s3_key"]) \
    .config("spark.hadoop.fs.s3a.secret.key", current_config["s3_secret"]) \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Caminho completo do S3 (input e output)
s3_input_path = f"s3a://{current_config['s3_bucket']}/{current_config['input_path']}"
s3_output_path = f"s3a://{current_config['s3_bucket']}/{current_config['output_path']}"

# Carregar o dataset do S3
df = spark.read.csv(s3_input_path, header=True, inferSchema=True)

# Processamento de dados: Adicionar coluna com a idade
processed_df = df.withColumn("age", year("created_at") - year("date_of_birth"))

# Exibir amostra do processamento
processed_df.show(10)

# Salvar os dados processados em Delta Table
processed_df.write.format("delta").mode("overwrite").save(s3_output_path)

print(f"Dados processados e salvos no Amazon S3 no caminho: {s3_output_path}")
spark.stop()
