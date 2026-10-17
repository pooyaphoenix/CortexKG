import sys
import os
import time

# --- Path Configuration ---
# Allows importing from the sibling 'app' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
app_dir = os.path.join(parent_dir, 'app')

if app_dir not in sys.path:
    sys.path.insert(0, app_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# --- App Imports ---
from config_manager import load_config
from llm_service import extract_knowledge, get_llm, build_system_instruction
from graph_service import initialize_graph, update_graph
from langchain_core.messages import SystemMessage, HumanMessage

# --- Local Imports ---
from scenarios import BENCHMARK_SUITE


def run_direct_llm(question: str, text_context: str, provider: str, model_name: str, api_key: str, base_url: str):
    """Baseline A: Raw LLM with plain text context window."""
    prompt = f"Context:\n{text_context}\n\nQuestion: {question}"
    llm = get_llm(provider, model_name, api_key, base_url, temperature=0.0)
    
    start_time = time.time()
    response = llm.invoke([HumanMessage(content=prompt)])
    latency = time.time() - start_time
    
    return response.content.strip(), latency


def run_cortex_kg(question: str, raw_texts: list[str], provider: str, model_name: str, api_key: str, base_url: str):
    """Approach B: CortexKG Knowledge Graph Extraction + Graph-Augmented RAG."""
    graph = initialize_graph()
    extraction_start = time.time()
    
    # 1. Extract Knowledge Triples and build graph
    for text in raw_texts:
        extracted_kg = extract_knowledge(
            text=text, 
            provider=provider, 
            model_name=model_name, 
            api_key=api_key, 
            base_url=base_url
        )
        graph = update_graph(graph, extracted_kg)
        
    extraction_time = time.time() - extraction_start

    # 2. Build system prompt with Structured Graph Context
    system_prompt = build_system_instruction(
        response_level="Medium",
        use_knowledge=True,
        graph=graph
    )
    
    # 3. Query LLM using Graph Memory
    llm = get_llm(provider, model_name, api_key, base_url, temperature=0.0)
    generation_start = time.time()
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=question)
    ])
    generation_time = time.time() - generation_start

    return response.content.strip(), len(graph.nodes), len(graph.edges), extraction_time, generation_time


def evaluate_answer(response: str, key_entities: list[str]) -> bool:
    """Checks if key target entities exist in the LLM response."""
    response_lower = response.lower()
    return all(entity.lower() in response_lower for entity in key_entities)


def main():
    cfg = load_config()
    provider = cfg["provider"]
    p_cfg = cfg["providers"][provider]
    
    model_name = p_cfg.get("model_name", "")
    api_key = p_cfg.get("api_key", "")
    base_url = p_cfg.get("base_url", "")
    
    print("==================================================================")
    print(f" 🚀 CORTEX_KG PERFORMANCE BENCHMARK")
    print(f" Provider: {provider} | Model: {model_name}")
    print("==================================================================\n")

    direct_correct = 0
    kg_correct = 0

    for idx, test in enumerate(BENCHMARK_SUITE):
        print(f"--- Scenario {idx + 1}: {test['name']} ---")
        print(f"Input Facts:\n  " + "\n  ".join(f"• {doc}" for doc in test['documents']))
        print(f"Query: \"{test['question']}\"\n")

        # Plain Text Execution
        full_text_context = "\n".join(test['documents'])
        direct_resp, direct_lat = run_direct_llm(
            test['question'], full_text_context, provider, model_name, api_key, base_url
        )
        direct_passed = evaluate_answer(direct_resp, test['key_entities'])
        if direct_passed: direct_correct += 1

        # CortexKG Execution
        kg_resp, nodes_cnt, edges_cnt, ext_time, gen_time = run_cortex_kg(
            test['question'], test['documents'], provider, model_name, api_key, base_url
        )
        kg_passed = evaluate_answer(kg_resp, test['key_entities'])
        if kg_passed: kg_correct += 1

        print(f"1️⃣ Plain Text Context (Raw Prompt):")
        print(f"   Response : {direct_resp}")
        print(f"   Accuracy : {'✅ Passed' if direct_passed else '❌ Failed'} | Latency: {direct_lat:.2f}s\n")

        print(f"2️⃣ CortexKG (Graph Memory Augmented):")
        print(f"   Extracted: {nodes_cnt} Nodes, {edges_cnt} Edges")
        print(f"   Response : {kg_resp}")
        print(f"   Accuracy : {'✅ Passed' if kg_passed else '❌ Failed'} | Time: {ext_time + gen_time:.2f}s (Ext: {ext_time:.2f}s)\n")
        print("-" * 66 + "\n")

    # Final Benchmark Summary
    total = len(BENCHMARK_SUITE)
    print("==================================================================")
    print(" 📊 FINAL BENCHMARK SUMMARY")
    print("==================================================================")
    print(f" Standard Text Prompting Accuracy : {(direct_correct / total) * 100:.1f}% ({direct_correct}/{total})")
    print(f" CortexKG Knowledge Graph Accuracy : {(kg_correct / total) * 100:.1f}% ({kg_correct}/{total})")
    print("==================================================================")


if __name__ == "__main__":
    main()