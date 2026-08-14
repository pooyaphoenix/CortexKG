import json
import os
import networkx as nx

from graph_service import initialize_graph, ensure_memory_metadata


MEMORY_FILE = "graph_memory.json"


def save_graph_to_disk(graph) -> None:
    """Saves the current NetworkX graph to a local JSON file."""
    try:
        ensure_memory_metadata(graph)

        data = nx.node_link_data(graph)

        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Error saving graph to disk: {e}")


def load_graph_from_disk():
    """Loads graph from local JSON and adds missing memory metadata."""

    if os.path.exists(MEMORY_FILE):

        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            graph = nx.node_link_graph(data)

            ensure_memory_metadata(graph)

            return graph

        except Exception as e:
            print(
                f"Error loading graph from disk: {e}. Starting fresh."
            )

    return initialize_graph()


def get_graph_export_json(graph) -> str:
    """Returns the graph as formatted JSON."""

    ensure_memory_metadata(graph)

    data = nx.node_link_data(graph)

    return json.dumps(
        data,
        indent=4,
        ensure_ascii=False
    )


def load_graph_from_json(json_str: str):
    """Converts uploaded JSON into a NetworkX graph."""

    data = json.loads(json_str)

    graph = nx.node_link_graph(data)

    ensure_memory_metadata(graph)

    return graph