from langgraph.graph import END, StateGraph
from sqlalchemy.orm import Session

from app.agents.nodes.completeness_check import completeness_check
from app.agents.nodes.duplicate_check import make_duplicate_check_node
from app.agents.nodes.extract_fields import extract_fields
from app.agents.nodes.preprocess_document import preprocess_document
from app.agents.nodes.risk_classification import risk_classification
from app.agents.state import ExtractionState


def build_extraction_graph(db: Session):
    graph = StateGraph(ExtractionState)

    graph.add_node("preprocess_document", preprocess_document)
    graph.add_node("extract_fields", extract_fields)
    graph.add_node("completeness_check", completeness_check)
    graph.add_node("risk_classification", risk_classification)
    graph.add_node("duplicate_check", make_duplicate_check_node(db))

    graph.set_entry_point("preprocess_document")
    graph.add_edge("preprocess_document", "extract_fields")
    graph.add_edge("extract_fields", "completeness_check")
    graph.add_edge("completeness_check", "risk_classification")
    graph.add_edge("risk_classification", "duplicate_check")
    graph.add_edge("duplicate_check", END)

    return graph.compile()
