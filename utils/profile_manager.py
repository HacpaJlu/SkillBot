from .json_helper import load_json, save_json
import os

PROFILES_DIR = os.path.join(os.getcwd(), 'profiles')

def list_profiles():
    if not os.path.exists(PROFILES_DIR):
        return []
    return [f[:-5] for f in os.listdir(PROFILES_DIR) if f.endswith('.json')]
