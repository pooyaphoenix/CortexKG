import json
import os
import threading
import copy
from typing import Dict, Any

CONFIG_FILE = "app_config.json"
_lock = threading.Lock()

# Define nested defaults for each provider
DEFAULT_CONFIG: Dict[str, Any] = {
    "provider": "Ollama (Local)",
    "response_level": "Medium",
    "graph_source": "User Input Only",
    "use_knowledge": True,
    "providers": {
        "Ollama (Local)": {
            "model_name": "gemma3:4b",
            "base_url": "http://localhost:11434",
            "api_key": ""
        },
        "Custom Provider": {
            "model_name": "gpt-5",
            "base_url": "",
            "api_key": ""
        },
        "OpenAI": {
            "model_name": "gpt-4o-mini",
            "base_url": "",
            "api_key": ""
        },
        "Google Gemini": {
            "model_name": "gemini-1.5-flash",
            "base_url": "",
            "api_key": ""
        }
    }
}

def load_config() -> Dict[str, Any]:
    """Reads configuration from JSON file with a deep-merge for nested provider settings."""
    with _lock:
        if not os.path.exists(CONFIG_FILE):
            _save_unlocked(DEFAULT_CONFIG)
            return copy.deepcopy(DEFAULT_CONFIG)
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            config = copy.deepcopy(DEFAULT_CONFIG)
            
            # Deep merge provider-specific settings
            if "providers" in data:
                for p_name, p_data in data["providers"].items():
                    if p_name in config["providers"] and isinstance(p_data, dict):
                        config["providers"][p_name].update(p_data)
            
            # Merge top-level global settings
            for key in ["provider", "response_level", "graph_source", "use_knowledge"]:
                if key in data:
                    config[key] = data[key]
                    
            return config
        except Exception as e:
            print(f"Warning: Failed to load {CONFIG_FILE}. Using defaults. Error: {e}")
            return copy.deepcopy(DEFAULT_CONFIG)

def save_config(config_dict: Dict[str, Any]) -> None:
    """Thread-safe function to save configuration dictionary to disk."""
    with _lock:
        _save_unlocked(config_dict)

def _save_unlocked(data: Dict[str, Any]) -> None:
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)