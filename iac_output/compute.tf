# Create a service plan
resource "azurerm_service_plan" "plan" {
  name                = "myproject-plan"
  resource_group_name = var.resource_group_name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "P1v2"
}

# Create a web app
resource "azurerm_linux_web_app" "app" {
  name                = var.app_service_name
  resource_group_name = var.resource_group_name
  location            = var.location
  service_plan_name   = azurerm_service_plan.plan.name

  site_config {
    linux_fx_version = "NODE|14-lts"
  }
}
