'''Integração via Ferramentas de ETL (Ex.: Informatica, Matillion ou Talend)
Extração dos Dados:

Configure um conector para Dynamics 365 que extrai os dados diretamente.
Armazenamento e Processamento:

Use o mesmo ETL para armazenar no Data Lake da Azure e processar diretamente no AWS Glue.
Script PySpark no Glue (Processamento Avançado):'''

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("GlueJob").getOrCreate()

# Carregar dados do S3
df = spark.read.json("s3://meu-bucket-s3/data/contacts.json")

# Transformação de dados
df_transformed = df.withColumnRenamed("contactid", "id").withColumnRenamed("fullname", "name")

# Gravar os dados processados no S3
df_transformed.write.mode("overwrite").parquet("s3://meu-bucket-s3/processed/contacts/")
