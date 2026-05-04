# Output database connection details
output "database_name" {
  value = azurerm_postgresql_database.myproject.name
}

output "database_username" {
  value = var.database_username
}

output "database_password" {
  value = var.database_password
  sensitive = true
}

output "database_host" {
  value = azurerm_postgresql_server.myproject.fqdn
}
