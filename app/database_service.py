import networkx as nx
from neo4j import GraphDatabase
from typing import Dict, Any, Tuple

def get_neo4j_driver(config: Dict[str, Any]):
    """Initializes and returns a Neo4j driver if enabled."""
    neo4j_cfg = config.get("neo4j", {})
    if not neo4j_cfg.get("enabled", False):
        return None
    
    uri = neo4j_cfg.get("uri", "bolt://localhost:7687")
    username = neo4j_cfg.get("username", "neo4j")
    password = neo4j_cfg.get("password", "")
    
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        driver.verify_connectivity()
        return driver
    except Exception as e:
        print(f"Neo4j connection error: {e}")
        return None

def test_neo4j_connection(config: Dict[str, Any]) -> Tuple[bool, str]:
    """Tests connection to Neo4j and returns status tuple (success, message)."""
    try:
        driver = get_neo4j_driver(config)
        if not driver:
            return False, "Neo4j is disabled or failed to initialize."
        driver.close()
        return True, "Successfully connected to Neo4j!"
    except Exception as e:
        return False, str(e)

def load_graph_from_neo4j(config: Dict[str, Any]) -> nx.DiGraph:
    """Loads nodes and relationships from Neo4j into a NetworkX DiGraph."""
    g = nx.DiGraph()
    driver = get_neo4j_driver(config)
    if not driver:
        return g
    
    neo4j_cfg = config.get("neo4j", {})
    db_name = neo4j_cfg.get("database", "neo4j")
    
    try:
        with driver.session(database=db_name) as session:
            # Load nodes
            node_result = session.run("MATCH (n) RETURN n")
            for record in node_result:
                node = record["n"]
                props = dict(node)
                node_id = props.get("id") or str(node.element_id)
                g.add_node(node_id, **props)
            
            # Load relationships
            rel_result = session.run("MATCH (a)-[r]->(b) RETURN a, type(r) as type, properties(r) as props, b")
            for record in rel_result:
                a_props = dict(record["a"])
                b_props = dict(record["b"])
                a_id = a_props.get("id")
                b_id = b_props.get("id")
                rel_type = record["type"]
                props = record["props"]
                
                if a_id and b_id:
                    g.add_edge(a_id, b_id, label=rel_type, **props)
    except Exception as e:
        print(f"Error loading graph from Neo4j: {e}")
    finally:
        driver.close()
        
    return g

def save_graph_to_neo4j(nx_graph: nx.DiGraph, config: Dict[str, Any]) -> bool:
    """Saves/upserts NetworkX nodes and relationships into Neo4j."""
    driver = get_neo4j_driver(config)
    if not driver:
        return False

    neo4j_cfg = config.get("neo4j", {})
    db_name = neo4j_cfg.get("database", "cortexKG")  # Default to cortexKG

    print(f"🔗 Syncing to Neo4j Database: '{db_name}' with {len(nx_graph.nodes)} nodes...")

    try:
        # Explicitly pass database name to session
        with driver.session(database=db_name) as session:
            # Upsert nodes
            for node_id, data in nx_graph.nodes(data=True):
                props = dict(data)
                props["id"] = str(node_id)
                session.run(
                    "MERGE (n {id: $id}) SET n +=$props",
                    id=str(node_id),
                    props=props
                )

            # Upsert relationships
            for u, v, data in nx_graph.edges(data=True):
                rel_type = data.get("label", "RELATED_TO").upper().replace(" ", "_")
                props = {k: v for k, v in data.items() if k != "label"}
                session.run(
                    f"""
                    MATCH (a {{id: $u_id}})
                    MATCH (b {{id: $v_id}})
                    MERGE (a)-[r:`{rel_type}`]->(b)
                    SET r += $props
                    """,
                    u_id=str(u),
                    v_id=str(v),
                    props=props
                )
        print("✅ Successfully synced graph to Neo4j!")
        return True
    except Exception as e:
        print(f"❌ Error saving graph to Neo4j: {e}")
        return False