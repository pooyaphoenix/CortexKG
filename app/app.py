import streamlit as st
from config_manager import load_config, save_config
from llm_service import generate_chat_stream, extract_knowledge
from graph_service import initialize_graph, update_graph
from ui_components import render_pyvis_graph, render_footer
from storage_service import (
    save_graph_to_disk, 
    load_graph_from_disk, 
    get_graph_export_json, 
    load_graph_from_json
)

st.set_page_config(page_title="CortexKG: LLM Knowledge Graph Explorer", layout="wide")

# --- Hide Streamlit Default UI ---
hide_streamlit_style = """
<style>
    /* Hides the "Deploy" button */
    .stAppDeployButton {display: none;}
    /* Hides the "..." menu in older versions */
    #MainMenu {visibility: hidden;}

</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- Callbacks for saving specific config sections ---
def update_global_setting(cfg_key, ui_key):
    cfg = load_config()
    cfg[cfg_key] = st.session_state[ui_key]
    save_config(cfg)

def update_provider_setting(provider_name, prop_key, ui_key):
    cfg = load_config()
    cfg["providers"][provider_name][prop_key] = st.session_state[ui_key]
    save_config(cfg)

# --- Load Configuration ---
app_cfg = load_config()
current_provider = app_cfg["provider"]
provider_list = list(app_cfg["providers"].keys())

# Ensure active provider exists in our list (fallback to index 0 if corrupted)
prov_idx = provider_list.index(current_provider) if current_provider in provider_list else 0

# --- Application State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "graph" not in st.session_state:
    st.session_state.graph = load_graph_from_disk()

# --- Sidebar Options ---
st.sidebar.title("⚙️ Settings")

st.sidebar.subheader("🤖 Model Provider")

# Global Provider Selection
st.sidebar.selectbox(
    "Select LLM Provider", 
    provider_list,
    index=prov_idx,
    key="ui_provider",
    on_change=update_global_setting,
    args=("provider", "ui_provider")
)

# Re-read active provider from config (in case the selectbox just updated it)
current_provider = app_cfg["provider"]
prov_cfg = app_cfg["providers"][current_provider]

# Provider-Specific Configurations
st.sidebar.markdown(f"**{current_provider} Settings**")

st.sidebar.text_input(
    "Model Name", 
    value=prov_cfg.get("model_name", ""),
    key=f"ui_{current_provider}_model",
    on_change=update_provider_setting,
    args=(current_provider, "model_name", f"ui_{current_provider}_model")
)

# Show Base URL only for Custom/Compatible endpoints and Ollama
if current_provider in ["Custom Provider", "Ollama (Local)"]:
    st.sidebar.text_input(
        "Base URL", 
        value=prov_cfg.get("base_url", ""),
        key=f"ui_{current_provider}_base",
        help="Custom endpoint (e.g., https://api.arvancloud.ir/v1 or http://localhost:11434)",
        on_change=update_provider_setting,
        args=(current_provider, "base_url", f"ui_{current_provider}_base")
    )

# Show API Key for everything EXCEPT local Ollama
if current_provider != "Ollama (Local)":
    api_key_val = prov_cfg.get("api_key", "")
    st.sidebar.text_input(
        f"API Key", 
        type="password",
        value=api_key_val,
        key=f"ui_{current_provider}_apikey",
        on_change=update_provider_setting,
        args=(current_provider, "api_key", f"ui_{current_provider}_apikey")
    )
    if not api_key_val and current_provider != "Custom Provider":
        st.sidebar.warning("Please enter an API Key to continue.")

st.sidebar.divider()

# Global Settings: Response Level & Extraction
response_level_opts = ["Short", "Medium", "Long"]
st.sidebar.select_slider(
    "Response Detail Level",
    options=response_level_opts,
    value=app_cfg["response_level"],
    key="ui_response_level",
    on_change=update_global_setting,
    args=("response_level", "ui_response_level")
)

graph_src_opts = ["User Input Only", "User Input + Model Response"]
st.sidebar.radio(
    "Build Graph From:",
    options=graph_src_opts,
    index=graph_src_opts.index(app_cfg["graph_source"]),
    key="ui_graph_source",
    on_change=update_global_setting,
    args=("graph_source", "ui_graph_source")
)

st.sidebar.divider()

# Global Settings: Context Injection
st.sidebar.subheader("🧠 Context Injection")
st.sidebar.toggle(
    "Use Graph as Knowledge Context", 
    value=app_cfg["use_knowledge"],
    key="ui_use_knowledge",
    on_change=update_global_setting,
    args=("use_knowledge", "ui_use_knowledge")
)

st.sidebar.divider()

# Graph Memory Controls
st.sidebar.subheader("💾 Graph Memory")
graph_json = get_graph_export_json(st.session_state.graph)
st.sidebar.download_button(
    label="⬇️ Export Graph as JSON",
    data=graph_json,
    file_name="my_knowledge_graph.json",
    mime="application/json",
    use_container_width=True
)

uploaded_file = st.sidebar.file_uploader("⬆️ Import Graph JSON", type=["json"])
if uploaded_file is not None:
    try:
        file_content = uploaded_file.read().decode("utf-8")
        st.session_state.graph = load_graph_from_json(file_content)
        save_graph_to_disk(st.session_state.graph)
        st.sidebar.success("Graph successfully imported!")
    except Exception as e:
        st.sidebar.error("Failed to import graph.")

# --- Application Header ---
st.title("CortexKG: LLM Knowledge Graph Explorer")
st.markdown(f"Provider: **`{current_provider}`** | Model: **`{prov_cfg.get('model_name','')}`**")

col1, col2 = st.columns([1, 1])

# Left Column: Chat Controller
with col1:
    st.subheader("Chat Interface")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("What would you like to discuss?"):
        
        # Pull latest active values for API call
        active_model = prov_cfg.get("model_name", "")
        active_api_key = prov_cfg.get("api_key", "")
        active_base_url = prov_cfg.get("base_url", "")
        
        if current_provider in ["OpenAI", "Google Gemini"] and not active_api_key:
            st.error(f"Cannot send message: {current_provider} API Key is missing.")
            st.stop()
            
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            
            try:
                stream = generate_chat_stream(
                    messages=api_messages, 
                    provider=current_provider,
                    model_name=active_model,
                    api_key=active_api_key,
                    base_url=active_base_url,
                    response_level=app_cfg["response_level"],
                    use_knowledge=app_cfg["use_knowledge"],
                    graph=st.session_state.graph
                )
                
                for chunk in stream:
                    if hasattr(chunk, "content"):
                        full_response += chunk.content
                        response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                with st.spinner("Extracting knowledge graph..."):
                    text_to_extract = f"User: {prompt}" if app_cfg["graph_source"] == "User Input Only" else f"User: {prompt}\nAssistant: {full_response}"

                    extracted_kg = extract_knowledge(
                        text=text_to_extract,
                        provider=current_provider,
                        model_name=active_model,
                        api_key=active_api_key,
                        base_url=active_base_url
                    )
                    
                    st.session_state.graph = update_graph(st.session_state.graph, extracted_kg)
                    save_graph_to_disk(st.session_state.graph)
                    st.rerun()

            except Exception as err:
                st.error(f"Error communicating with {current_provider}: {err}")
                st.session_state.messages.pop()

# Right Column: Graph Visualizer
with col2:
    st.subheader("Interactive Graph")
    
    # Confirmation Popover before clearing memory
    with st.popover("Clear Graph Memory & Chat", use_container_width=True):
        st.warning("⚠️ Are you sure? This will permanently wipe the active knowledge graph and chat history.")
        if st.button("Yes, Clear Everything", type="primary", use_container_width=True):
            st.session_state.graph = initialize_graph()
            save_graph_to_disk(st.session_state.graph) 
            st.session_state.messages = []
            st.rerun()
            
    render_pyvis_graph(st.session_state.graph)

    render_footer(
        developer_name="Pooya Chavoshi", 
        github_url="https://github.com/pooyachavoshi"
    )