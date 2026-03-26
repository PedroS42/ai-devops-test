provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "meu_grupo" {
  name     = "rg-estagio-devscope"
  location = "West Europe"
}

resource "azurerm_storage_account" "meu_armazenamento" {
  name                     = "storageestagiodevscope"
  resource_group_name      = azurerm_resource_group.meu_grupo.name
  location                 = azurerm_resource_group.meu_grupo.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "tfstatestoragedevscope"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}
