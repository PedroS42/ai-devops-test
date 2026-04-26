# Output the storage account URL
output "storage_account_url" {
  value = azurerm_storage_account.storage.primary_web_endpoint
}

# Output the web app URL
output "web_app_url" {
  value = azurerm_linux_web_app.app.default_hostname
}

# Output the database connection string
output "database_connection_string" {
  value = "host=${azurerm_postgresql_server.database.fqdn} port=5432 dbname=${azurerm_postgresql_database.db.name} user=${var.database_username} password=${var.database_password} sslmode=require"
  sensitive = true
}
