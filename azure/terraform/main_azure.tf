## main.tf

provider "azurerm" {
    features {}
}

variable "environment" {
    description = "Environment name(dev, homolog, prod)"
    type        = string  
}

module "vnet" {
    source     = "./modules/vnet"
    enviroment = var.environment 
}

module "key vault" {
    source     = "./modules/key_vault"
    enviroment = var.environment 
}

module "databricks" {
    source     = "./modules/databricks"
    enviroment = var.environment
}

module "data_factory" {
    source     = "./modules/data_factory"
    enviroment = var.environment
}

module "data_lake" {
    source     = "./modules/data_lake"
    enviroment = var.environment
}

module "sql_database" {
    source = "./modules/sql_database"
    enviroment = var.environment
}

module "sevice_bus" {
    source = "./modules/service_bus"
    enviroment = var.environment
}

module "api_service" {
    source = "./modules/api_service"
    enviroment = var.environment
}

module  "dynamics_365" {
    source = "./modules/dynamics_365"
    enviroment = var.environment
}

## modules/vnet/main_azure.tf
resource "azurerm_virtual_network" "vnet" {
    name = "vnet-${var.environment}"
    location = "eastus"
    resource_group_name = "rg-${var.environment}"
    address_space = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "subnet" {
    name = "subnet-${var.environment}"
    resource_group_name = azurerm_virtual_network.vnet.resource_group_name
    virtual_network_name = azurerm_virtual_network.vnet.name
    address_prefixes = ["10.0.1.0/24"]
}

## modules/key_vault/main.tf
resource "azurerm_key_vault" "key_vault" {
  name                        = "keyvault-${var.environment}"
  location                    = "eastus"
  resource_group_name         = "rg-${var.environment}"
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"
  soft_delete_enabled         = true
}
## modules/databricks/main.tf
resource "azurerm_databricks_workspace" "databricks" {
  name                = "databricks-${var.environment}"
  location            = "eastus"
  resource_group_name = "rg-${var.environment}"
  sku                 = "standard"
}

## modules/data_factory/main.tf
resource "azurerm_data_factory" "data_factory" {
  name                = "datafactory-${var.environment}"
  location            = "eastus"
  resource_group_name = "rg-${var.environment}"
}

## modules/data_lake/main.tf
resource "azurerm_storage_account" "data_lake" {
  name                     = "datalake${var.environment}"
  resource_group_name      = "rg-${var.environment}"
  location                 = "eastus"
  account_tier             = "Standard"
  account_replication_type = "LRS"
  enable_hierarchical_namespace = true
}

## modules/sql_database/main.tf
resource "azurerm_sql_server" "sql_server" {
  name                         = "sqlserver-${var.environment}"
  resource_group_name          = "rg-${var.environment}"
  location                     = "eastus"
  version                      = "12.0"
  administrator_login          = "adminuser"
  administrator_login_password = "AdminPassword123!"
}

resource "azurerm_sql_database" "sql_database" {
  name                = "sqldb-${var.environment}"
  resource_group_name = azurerm_sql_server.sql_server.resource_group_name
  server_name         = azurerm_sql_server.sql_server.name
  sku_name            = "Basic"
}

## modules/service_bus/main.tf
resource "azurerm_servicebus_namespace" "service_bus" {
  name                = "servicebus-${var.environment}"
  location            = "eastus"
  resource_group_name = "rg-${var.environment}"
  sku                 = "Standard"
}

resource "azurerm_servicebus_queue" "queue" {
  name                = "queue-${var.environment}"
  resource_group_name = azurerm_servicebus_namespace.service_bus.resource_group_name
  namespace_name      = azurerm_servicebus_namespace.service_bus.name
}

## modules/api_service/main.tf
resource "azurerm_api_management" "api_service" {
  name                = "apim-${var.environment}"
  location            = "eastus"
  resource_group_name = "rg-${var.environment}"
  publisher_name      = "API Publisher"
  publisher_email     = "api-publisher@example.com"
  sku_name            = "Developer_1"
}

## modules/dynamics_365/main.tf
resource "azurerm_logic_app_workflow" "dynamics_connector" {
  name                = "dynamics-${var.environment}"
  location            = "eastus"
  resource_group_name = "rg-${var.environment}"
}

resource "azurerm_logic_app_trigger_http_request" "http_trigger" {
  name      = "http-trigger"
  logic_app_id = azurerm_logic_app_workflow.dynamics_connector.id
}

resource "azurerm_logic_app_action_http" "dynamics_action" {
  name      = "dynamics-action"
  logic_app_id = azurerm_logic_app_workflow.dynamics_connector.id
  method    = "GET"
  uri       = "https://your-dynamics-365-instance-url"
}