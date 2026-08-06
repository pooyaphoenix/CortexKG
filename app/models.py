from pydantic import BaseModel

class Node(BaseModel):
    id: str
    label: str
    entity_type: str

class Edge(BaseModel):
    source: str
    target: str
    relation: str

class KnowledgeGraph(BaseModel):
    nodes: list[Node]
    edges: list[Edge]