# Define input variables
variable "environment" {
  type        = string
  description = "Environment name"
}

variable "location" {
  type        = string
  description = "Location for all resources"
}

variable "resource_group_name" {
  type        = string
  description = "Resource group name"
}

variable "storage_account_name" {
  type        = string
  description = "Storage account name"
}

variable "app_service_name" {
  type        = string
  description = "App service name"
}

variable "database_name" {
  type        = string
  description = "Database name"
}

variable "database_username" {
  type        = string
  description = "Database username"
}

variable "database_password" {
  type        = string
  sensitive   = true
  description = "Database password"
}
