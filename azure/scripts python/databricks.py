from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, current_timestamp

# Inicializando a Spark Session
spark = SparkSession.builder \
    .appName("Data Processing - Azure to AWS") \
    .getOrCreate()

# Configurações do ADLS (Azure Data Lake Storage)
adls_account_name = "<seu-adls-account-name>"
adls_container_name = "<seu-container-name>"
adls_sas_token = "<seu-sas-token>"  # Para autenticação
adls_url = f"abfss://{adls_container_name}@{adls_account_name}.dfs.core.windows.net/<seu-diretorio>"

# Configurações do S3 (AWS)
s3_bucket_name = "<seu-bucket-s3>"
s3_output_path = f"s3://{s3_bucket_name}/processed-data/"

# Lendo os dados do Azure Data Lake (ADLS)
df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(adls_url)

print("Dados carregados do ADLS:")
df.show()

# Processamento básico (adicionar timestamp e filtrar colunas nulas)
df_processed = df.withColumn("processed_at", current_timestamp()) \
    .filter(col("email").isNotNull())

print("Dados após processamento:")
df_processed.show()

# Salvando os dados no S3 (AWS)
df_processed.write.format("parquet") \
    .mode("overwrite") \
    .save(s3_output_path)

print(f"Dados processados salvos no S3 em: {s3_output_path}")

# Parar a Spark Session
spark.stop()
