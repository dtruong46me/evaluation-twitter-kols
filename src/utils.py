import os, sys
import yaml

def load_config():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    
    return config

if __name__=='__main__':
    print(load_config())