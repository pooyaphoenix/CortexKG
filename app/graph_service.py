import networkx as nx
from models import KnowledgeGraph

def initialize_graph() -> nx.DiGraph:
    """Creates a new empty directed graph."""
    return nx.DiGraph()

def update_graph(nx_graph: nx.DiGraph, kg: KnowledgeGraph) -> nx.DiGraph:
    """Idempotently adds new nodes and edges to the NetworkX graph."""
    for node in kg.nodes:
        nx_graph.add_node(
            node.id, 
            label=node.label, 
            title=f"Type: {node.entity_type}",
            shape="dot",
            size=20
        )
        
    for edge in kg.edges:
        # Prevent floating edges by validating both source and target exist
        if edge.source in nx_graph.nodes and edge.target in nx_graph.nodes:
            nx_graph.add_edge(
                edge.source, 
                edge.target, 
                label=edge.relation,
                title=edge.relation
            )
            
    return nx_graph