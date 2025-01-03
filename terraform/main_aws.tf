## main.tf
provider "aws" {
  region = var.region
}

variable "environment" {
  description = "Environment name (dev, homolog, prod)"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

module "vpc" {
  source      = "./modules/vpc"
  environment = var.environment
  region      = var.region
}

module "secrets_manager" {
  source      = "./modules/secrets_manager"
  environment = var.environment
  region      = var.region
}

module "databricks" {
  source      = "./modules/databricks"
  environment = var.environment
  region      = var.region
}

module "glue" {
  source      = "./modules/glue"
  environment = var.environment
  region      = var.region
}

module "s3_data_lake" {
  source      = "./modules/s3_data_lake"
  environment = var.environment
  region      = var.region
}

module "rds" {
  source      = "./modules/rds"
  environment = var.environment
  region      = var.region
}

module "sns" {
  source      = "./modules/sns"
  environment = var.environment
  region      = var.region
}

module "api_gateway" {
  source      = "./modules/api_gateway"
  environment = var.environment
  region      = var.region
}

module "dynamics_365" {
  source      = "./modules/dynamics_365"
  environment = var.environment
  region      = var.region
}

## modules/vpc/main.tf
resource "aws_vpc" "vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "vpc-${var.environment}"
  }
}

resource "aws_subnet" "subnet" {
  vpc_id     = aws_vpc.vpc.id
  cidr_block = "10.0.1.0/24"
  tags = {
    Name = "subnet-${var.environment}"
  }
}

## modules/secrets_manager/main.tf
resource "aws_secretsmanager_secret" "key_vault" {
  name = "secrets-${var.environment}"
}

## modules/databricks/main.tf
resource "aws_emr_cluster" "databricks" {
  name          = "databricks-${var.environment}"
  release_label = "emr-6.3.0"
  applications  = ["Spark"]
  ec2_attributes {
    subnet_id = module.vpc.subnet_id
  }
}

## modules/glue/main.tf
resource "aws_glue_catalog_database" "glue_database" {
  name = "glue-${var.environment}"
}

## modules/s3_data_lake/main.tf
resource "aws_s3_bucket" "data_lake" {
  bucket = "datalake-${var.environment}"
  acl    = "private"
}

## modules/rds/main.tf
resource "aws_db_instance" "rds" {
  identifier         = "rds-${var.environment}"
  engine             = "mysql"
  instance_class     = "db.t3.micro"
  allocated_storage  = 20
  username           = "adminuser"
  password           = "AdminPassword123!"
  skip_final_snapshot = true
}

## modules/sns/main.tf
resource "aws_sns_topic" "sns" {
  name = "sns-${var.environment}"
}

## modules/api_gateway/main.tf
resource "aws_api_gateway_rest_api" "api_gateway" {
  name = "api-${var.environment}"
}

resource "aws_api_gateway_resource" "resource" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  parent_id   = aws_api_gateway_rest_api.api_gateway.root_resource_id
  path_part   = "path"
}

resource "aws_api_gateway_method" "method" {
  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
  resource_id   = aws_api_gateway_resource.resource.id
  http_method   = "GET"
  authorization = "NONE"
}

## modules/dynamics_365/main.tf
resource "aws_lambda_function" "dynamics_connector" {
  function_name = "dynamics-${var.environment}"
  runtime       = "nodejs14.x"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "index.handler"
  code {
    s3_bucket = "dynamics-code-bucket"
    s3_key    = "lambda-dynamics.zip"
  }
}

resource "aws_api_gateway_integration" "integration" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  resource_id = aws_api_gateway_resource.resource.id
  http_method = aws_api_gateway_method.method.http_method
  type        = "AWS_PROXY"
  uri         = aws_lambda_function.dynamics_connector.invoke_arn
}