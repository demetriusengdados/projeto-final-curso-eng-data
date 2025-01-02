'''Processamento no AWS Glue:

No Glue, crie um Job PySpark para processar os dados.'''

import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame

glueContext = GlueContext(SparkContext.getOrCreate())

# Carregar dados do S3
datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://meu-bucket-s3/data/contacts.json"]},
    format="json"
)

# Transformações
datasource = datasource.toDF()
datasource = datasource.withColumnRenamed("contactid", "id").withColumnRenamed("fullname", "name")

# Gravar dados processados no S3
datasource.write.mode("overwrite").parquet("s3://meu-bucket-s3/processed/contacts/")

'''Devolução ao Dynamics 365:

Use um script Python com a API REST para enviar os dados de volta.'''