import networkx as nx
from models import KnowledgeGraph
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

SYSTEM_PROMPTS = {
    "Short": "Keep your response extremely concise, direct, and brief (1 sentences max).",
    "Medium": "Provide a balanced, clear, and moderately detailed response. (2-3 sentences max).",
    "Long": "Provide a detailed, comprehensive, and in-depth explanation with complete context."
}

def get_llm(
    provider: str,
    model_name: str,
    api_key: str = None,
    base_url: str = None,
    temperature: float = 0.7,
    max_tokens: int | None = None,
):
    """Factory function to initialize the correct LangChain model based on provider and optional base_url.

    max_tokens is translated to each backend's native parameter name:
      - OpenAI / Custom Provider (OpenAI-compatible): `max_tokens`
      - Google Gemini:                                `max_output_tokens`
      - Ollama:                                        `num_predict`
    """

    # 1. OpenAI or OpenAI-Compatible APIs (ArvanCloud, OpenRouter, vLLM, LM Studio, etc.)
    if provider in ["OpenAI", "Custom Provider"]:
        from langchain_openai import ChatOpenAI
        kwargs = {
            "model": model_name,
            "api_key": api_key if api_key else "not-needed", # Some custom local endpoints don't strictly require a key
            "temperature": temperature
        }
        if max_tokens:
            kwargs["max_tokens"] = max_tokens
        if base_url and base_url.strip():
            kwargs["base_url"] = base_url.strip()
        return ChatOpenAI(**kwargs)

    # 2. Google Gemini
    elif provider == "Google Gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        kwargs = {
            "model": model_name,
            "google_api_key": api_key,
            "temperature": temperature
        }
        if max_tokens:
            kwargs["max_output_tokens"] = max_tokens
        return ChatGoogleGenerativeAI(**kwargs)

    # 3. Ollama (Local or Remote Server)
    else:
        from langchain_ollama import ChatOllama
        kwargs = {"model": model_name, "temperature": temperature}
        if max_tokens:
            kwargs["num_predict"] = max_tokens
        if base_url and base_url.strip():
            kwargs["base_url"] = base_url.strip()
        return ChatOllama(**kwargs)

def format_messages_for_langchain(messages: list[dict], system_instruction: str):
    """Converts basic dictionary messages into LangChain message objects."""
    lc_messages = [SystemMessage(content=system_instruction)]
    for msg in messages:
        if msg["role"] == "user":
            lc_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            lc_messages.append(AIMessage(content=msg["content"]))
    return lc_messages

def build_system_instruction(
    response_level: str,
    system_prompt: str = "",
    use_knowledge: bool = False,
    graph: nx.Graph = None,
) -> str:
    """Builds the final system instruction.

    If a custom system_prompt is provided (non-empty after stripping), it takes
    full precedence over the response-level default. The knowledge graph context
    (if enabled) is appended afterward in either case.
    """
    if system_prompt and system_prompt.strip():
        system_instruction = system_prompt.strip()
    else:
        system_instruction = SYSTEM_PROMPTS.get(response_level, SYSTEM_PROMPTS["Medium"])

    if use_knowledge and graph is not None:
        graph_context = "\n\n--- KNOWLEDGE GRAPH CONTEXT ---\n"
        if len(graph.nodes) == 0:
            graph_context += "The graph is currently empty.\n"
        else:
            graph_context += f"Entities: {', '.join([str(n) for n in graph.nodes])}\n\n"
            if len(graph.edges) > 0:
                graph_context += "Relationships:\n"
                for u, v, data in graph.edges(data=True):
                    relation = data.get("label", "RELATED_TO")
                    graph_context += f"- {u} --[{relation}]--> {v}\n"

        graph_context += "\nUse the above relationships as factual context to answer the user's queries."
        system_instruction += graph_context

    return system_instruction

def generate_chat_stream(
    messages: list[dict],
    provider: str,
    model_name: str,
    api_key: str = None,
    base_url: str = None,
    response_level: str = "Medium",
    use_knowledge: bool = False,
    graph: nx.Graph = None,
    temperature: float = 0.7,
    max_tokens: int | None = None,
    system_prompt: str = "",
):
    """Streams conversational response using LangChain."""
    system_instruction = build_system_instruction(
        response_level=response_level,
        system_prompt=system_prompt,
        use_knowledge=use_knowledge,
        graph=graph
    )

    formatted_messages = format_messages_for_langchain(messages, system_instruction)

    llm = get_llm(
        provider=provider,
        model_name=model_name,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return llm.stream(formatted_messages)

def extract_knowledge(text: str, provider: str, model_name: str, api_key: str = None, base_url: str = None) -> KnowledgeGraph:
    """Uses LangChain structured output to extract nodes and edges uniformly across endpoints.

    Deliberately does NOT use the user's configured temperature/max_tokens: extraction
    needs temperature=0.0 for determinism, and constraining max_tokens here risks
    truncating the structured JSON output before it parses correctly.
    """
    prompt = f"""Extract exact entities (names, places, jobs, concepts) and their relationships.
- Use exact lowercase terms (e.g., "ali", "germany", "computer engineer"). 
- DO NOT use generic categories like "person" or "location".

Example: "Ali loves Germany" -> Nodes: ["ali", "germany"], Edge: "ali" -> "loves" -> "germany"

Text: {text}"""

    try:
        llm = get_llm(provider=provider, model_name=model_name, api_key=api_key, base_url=base_url, temperature=0.0)
        structured_llm = llm.with_structured_output(KnowledgeGraph)
        result = structured_llm.invoke(prompt)

        return result if result else KnowledgeGraph(nodes=[], edges=[])
    except Exception as e:
        print(f"Error extracting knowledge: {e}")
        return KnowledgeGraph(nodes=[], edges=[])