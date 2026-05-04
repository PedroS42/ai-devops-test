import yaml
import os

CONFIG_FILE = 'config.yml'

def load_config():
    """Load the configuration from the YAML file."""
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f) or {}

def update_config(feature, new_model):
    """Update a specific feature's model in the configuration file."""
    config = load_config()
    config[feature] = new_model
    with open(CONFIG_FILE, 'w') as f:
        yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)

