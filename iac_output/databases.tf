# Create a PostgreSQL server
resource "azurerm_postgresql_server" "database" {
  name                = "myproject-postgres"
  resource_group_name = var.resource_group_name
  location            = var.location
  sku_name            = "GP_Gen5_2"

  storage_mb                   = 5120
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = true

  administrator_login          = var.database_username
  administrator_login_password = var.database_password
  version                      = "11"
}

# Create a PostgreSQL database
resource "azurerm_postgresql_database" "db" {
  name  = var.database_name
  resource_group_name = var.resource_group_name
  server_name = azurerm_postgresql_server.database.name
  charset   = "UTF8"
  collation = "English_United States.1252"
}
