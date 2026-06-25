# Create resource group
resource "azurerm_resource_group" "myproject" {
  name     = var.resource_group_name
  location = var.location
}

# Create PostgreSQL database
resource "azurerm_postgresql_server" "myproject" {
  name                = var.database_name
  location            = azurerm_resource_group.myproject.location
  resource_group_name = azurerm_resource_group.myproject.name

  sku_name = "GP_Gen5_2"

  storage_mb                   = 5120
  backup_retention_days        = 7
  geo_redundant_backup_enabled   = false
  infrastructure_encryption_enabled = false

  administrator_login          = var.database_username
  administrator_login_password  = var.database_password
  version                       = "11"
}

resource "azurerm_postgresql_database" "myproject" {
  name                = "myprojectdb"
  resource_group_name = azurerm_resource_group.myproject.name
  server_name         = azurerm_postgresql_server.myproject.name
  charset             = "UTF8"
  collation           = "English_United States.1252"
}
