import json
import os
import networkx as nx
from graph_service import initialize_graph

# The local file where the graph will be permanently saved
MEMORY_FILE = "graph_memory.json"

def save_graph_to_disk(graph) -> None:
    """Saves the current NetworkX graph to a local JSON file."""
    try:
        data = nx.node_link_data(graph)
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving graph to disk: {e}")

def load_graph_from_disk():
    """Loads the graph from the local JSON file. If missing, initializes a new one."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return nx.node_link_graph(data)
        except Exception as e:
            print(f"Error loading graph from disk: {e}. Starting fresh.")
    
    return initialize_graph()

def get_graph_export_json(graph) -> str:
    """Returns the graph as a formatted JSON string for user download."""
    data = nx.node_link_data(graph)
    return json.dumps(data, indent=4)

def load_graph_from_json(json_str: str):
    """Converts an uploaded JSON string back into a NetworkX graph."""
    data = json.loads(json_str)
    return nx.node_link_graph(data)