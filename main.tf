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

  # Necessary so we dont allow public access to the storage account, only those with the right permissions
  allow_nested_items_to_be_public = false
}