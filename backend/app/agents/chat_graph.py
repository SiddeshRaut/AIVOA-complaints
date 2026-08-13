from collections.abc import AsyncGenerator

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph

from app.agents.prompts.chat_prompt import CHAT_SYSTEM_PROMPT, build_chat_context
from app.agents.state import ChatState
from app.config import get_settings
from app.services.groq_client import get_chat_model


def retrieve_context(state: ChatState) -> dict:
    context = build_chat_context(state.get("document_text", ""), state.get("form_snapshot"))
    return {"context": context}


async def generate_answer(state: ChatState) -> dict:
    settings = get_settings()
    # streaming=True so token callbacks fire even though ainvoke returns the full message;
    # astream_events() on the compiled graph (below) surfaces those as on_chat_model_stream.
    llm = get_chat_model(settings.groq_chat_model, temperature=0.2, streaming=True)

    messages: list = [SystemMessage(content=f"{CHAT_SYSTEM_PROMPT}\n\n{state['context']}")]
    for turn in state.get("history", []):
        if turn.get("role") == "user":
            messages.append(HumanMessage(content=turn["content"]))
        else:
            messages.append(AIMessage(content=turn["content"]))
    messages.append(HumanMessage(content=state["message"]))

    response = await llm.ainvoke(messages)
    return {"answer": str(response.content)}


def build_chat_graph():
    graph = StateGraph(ChatState)
    graph.add_node("retrieve_context", retrieve_context)
    graph.add_node("generate_answer", generate_answer)
    graph.set_entry_point("retrieve_context")
    graph.add_edge("retrieve_context", "generate_answer")
    graph.add_edge("generate_answer", END)
    return graph.compile()


async def stream_chat_answer(
    message: str, document_text: str, form_snapshot: dict | None, history: list[dict]
) -> AsyncGenerator[str, None]:
    """Runs the compiled chat graph and re-emits the generate_answer node's token
    stream as it happens, via LangGraph's astream_events — real LLM token streaming,
    unlike the artificially-staggered field events used for extraction.
    """
    graph = build_chat_graph()
    inputs: ChatState = {
        "message": message,
        "document_text": document_text,
        "form_snapshot": form_snapshot or {},
        "history": history,
    }

    async for event in graph.astream_events(inputs, version="v2"):
        if event["event"] == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if chunk.content:
                yield str(chunk.content)
