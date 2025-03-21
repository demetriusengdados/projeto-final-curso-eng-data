'''Armazenamento no Data Lake (Azure):

Os dados extraídos são armazenados no Azure Data Lake como arquivos JSON ou CSV.
Transferência para AWS Glue:

Configure o AWS DataSync ou crie um script em AWS SDK (boto3) 
para transferir os arquivos do Data Lake para um bucket S3.'''

import boto3

s3 = boto3.client('s3')
bucket_name = "meu-bucket-s3"
file_path = "contacts.json"

s3.upload_file(file_path, bucket_name, "data/contacts.json")
