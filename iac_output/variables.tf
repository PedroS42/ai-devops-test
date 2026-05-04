# Define input variables
variable "environment" {
  type        = string
  description = "Environment name"
}

variable "location" {
  type        = string
  description = "Azure location"
}

variable "resource_group_name" {
  type        = string
  description = "Resource group name"
}

variable "database_name" {
  type        = string
  description = "PostgreSQL database name"
}

variable "database_username" {
  type        = string
  description = "PostgreSQL database username"
}

variable "database_password" {
  type        = string
  sensitive   = true
  description = "PostgreSQL database password"
}
