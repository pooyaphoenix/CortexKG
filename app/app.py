import copy

import streamlit as st
from config_manager import DEFAULT_CONFIG, load_config, save_config
from llm_service import generate_chat_stream, extract_knowledge
from graph_service import initialize_graph, update_graph
from ui_components import render_pyvis_graph, render_3d_graph, render_footer, render_memory_manager
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

def set_provider_value(provider_name, prop_key, value):
    """Directly sets a provider config value (used by preset buttons, which aren't tied to a widget key)."""
    cfg = load_config()
    cfg["providers"][provider_name][prop_key] = value
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

# ===========================================================
# Model & Connection — always visible, this is what you need
# to actually send a message
# ===========================================================
with st.sidebar.container(border=True):

    st.subheader("🤖 Model & Connection")

    st.selectbox(
        "LLM Provider",
        provider_list,
        index=prov_idx,
        key="ui_provider",
        on_change=update_global_setting,
        args=("provider", "ui_provider")
    )

    # Re-read active provider from config (in case the selectbox just updated it)
    current_provider = app_cfg["provider"]
    prov_cfg = app_cfg["providers"][current_provider]

    st.text_input(
        "Model Name",
        value=prov_cfg.get("model_name", ""),
        key=f"ui_{current_provider}_model",
        on_change=update_provider_setting,
        args=(current_provider, "model_name", f"ui_{current_provider}_model")
    )

    if current_provider in ["Custom Provider", "Ollama (Local)"]:
        st.text_input(
            "Base URL",
            value=prov_cfg.get("base_url", ""),
            key=f"ui_{current_provider}_base",
            help="Custom endpoint (e.g., https://api.arvancloud.ir/v1 or http://localhost:11434)",
            on_change=update_provider_setting,
            args=(current_provider, "base_url", f"ui_{current_provider}_base")
        )

    if current_provider != "Ollama (Local)":
        api_key_val = prov_cfg.get("api_key", "")
        st.text_input(
            "API Key",
            type="password",
            value=api_key_val,
            key=f"ui_{current_provider}_apikey",
            on_change=update_provider_setting,
            args=(current_provider, "api_key", f"ui_{current_provider}_apikey")
        )
        if not api_key_val and current_provider != "Custom Provider":
            st.warning("Please enter an API Key to continue.")

# ===========================================================
# Generation & Prompt — advanced, collapsed by default
# ===========================================================
with st.sidebar.expander("🎛️ Generation & Prompt"):

    st.caption("Quick temperature presets")
    preset_col1, preset_col2, preset_col3 = st.columns(3)

    with preset_col1:
        if st.button("🎯 Precise", use_container_width=True, help="Sets temperature to 0.2"):
            set_provider_value(current_provider, "temperature", 0.2)
            st.rerun()

    with preset_col2:
        if st.button("⚖️ Balanced", use_container_width=True, help="Sets temperature to 0.7"):
            set_provider_value(current_provider, "temperature", 0.7)
            st.rerun()

    with preset_col3:
        if st.button("🎨 Creative", use_container_width=True, help="Sets temperature to 1.3"):
            set_provider_value(current_provider, "temperature", 1.3)
            st.rerun()

    temp_value = float(prov_cfg.get("temperature", 0.7))
    st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        step=0.1,
        value=temp_value,
        key=f"ui_{current_provider}_temperature",
        on_change=update_provider_setting,
        args=(current_provider, "temperature", f"ui_{current_provider}_temperature")
    )
    if temp_value <= 0.3:
        st.caption("🎯 Focused & deterministic")
    elif temp_value <= 1.0:
        st.caption("⚖️ Balanced")
    else:
        st.caption("🎨 Creative & varied")

    st.number_input(
        "Max Tokens",
        min_value=1,
        max_value=128000,
        step=64,
        value=int(prov_cfg.get("max_tokens", 2048)),
        key=f"ui_{current_provider}_maxtokens",
        help="Maximum number of tokens the model may generate in a single response.",
        on_change=update_provider_setting,
        args=(current_provider, "max_tokens", f"ui_{current_provider}_maxtokens")
    )

    st.divider()

    response_level_opts = ["Short", "Medium", "Long"]
    st.select_slider(
        "Response Detail Level",
        options=response_level_opts,
        value=app_cfg["response_level"],
        key="ui_response_level",
        help="Ignored whenever a custom System Prompt is set below.",
        on_change=update_global_setting,
        args=("response_level", "ui_response_level")
    )

    system_prompt_val = app_cfg.get("system_prompt", "")
    st.text_area(
        "Custom System Prompt (optional)",
        value=system_prompt_val,
        key="ui_system_prompt",
        height=100,
        placeholder="e.g., You are a senior backend engineer who always replies with concrete code examples.",
        on_change=update_global_setting,
        args=("system_prompt", "ui_system_prompt")
    )

    if system_prompt_val.strip():
        st.caption("🟢 Using your custom system prompt — overrides Response Detail Level.")
    else:
        st.caption("⚪ Using the default prompt based on Response Detail Level.")

# ===========================================================
# Knowledge Graph Behavior
# ===========================================================
with st.sidebar.expander("🧠 Knowledge Graph Behavior"):

    st.toggle(
        "Use Graph as Knowledge Context",
        value=app_cfg["use_knowledge"],
        key="ui_use_knowledge",
        on_change=update_global_setting,
        args=("use_knowledge", "ui_use_knowledge")
    )

    graph_src_opts = ["User Input Only", "User Input + Model Response"]
    st.radio(
        "Build Graph From:",
        options=graph_src_opts,
        index=graph_src_opts.index(app_cfg["graph_source"]),
        key="ui_graph_source",
        on_change=update_global_setting,
        args=("graph_source", "ui_graph_source")
    )

# ===========================================================
# Data & Memory
# ===========================================================
with st.sidebar.expander("💾 Data & Memory"):

    graph_json = get_graph_export_json(st.session_state.graph)
    st.download_button(
        label="⬇️ Export Graph as JSON",
        data=graph_json,
        file_name="my_knowledge_graph.json",
        mime="application/json",
        use_container_width=True
    )

    uploaded_file = st.file_uploader("⬆️ Import Graph JSON", type=["json"])
    if uploaded_file is not None:
        try:
            file_content = uploaded_file.read().decode("utf-8")
            st.session_state.graph = load_graph_from_json(file_content)
            save_graph_to_disk(st.session_state.graph)
            st.success("Graph successfully imported!")
        except Exception as e:
            st.error("Failed to import graph.")

    st.divider()
    st.markdown("**♻️ Danger Zone**")

    with st.popover("Reset All Settings", use_container_width=True):

        st.warning(
            "⚠️ Are you sure? "
            "This will restore every setting to its default value."
        )

        if st.button("Yes, Reset Settings", type="primary", use_container_width=True):
            save_config(copy.deepcopy(DEFAULT_CONFIG))
            st.rerun()

# --- Application Header ---
st.title("CortexKG: LLM Knowledge Graph Explorer")
st.markdown(f"Provider: **`{current_provider}`** | Model: **`{prov_cfg.get('model_name','')}`**")

tab_chat, tab_graph, tab_memory = st.tabs(
    [
        "💬 Chat",
        "🕸️ Graph",
        "🧠 Memory"
    ]
)

with tab_chat:

    st.subheader("Chat Interface")

    with st.popover("Clear Chat", use_container_width=True):
        st.warning(
            "⚠️ Are you sure? "
            "This will erase the chat history "
            "but keep the knowledge graph intact."
        )
        if st.button("Yes, Clear Chat", type="primary", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("What would you like to discuss?"):

        active_model = prov_cfg.get("model_name", "")
        active_api_key = prov_cfg.get("api_key", "")
        active_base_url = prov_cfg.get("base_url", "")
        active_temperature = prov_cfg.get("temperature", 0.7)
        active_max_tokens = prov_cfg.get("max_tokens", 2048)
        active_system_prompt = app_cfg.get("system_prompt", "")

        if current_provider in ["OpenAI", "Google Gemini"] and not active_api_key:
            st.error(f"Cannot send message: {current_provider} API Key is missing.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            response_placeholder = st.empty()
            full_response = ""

            api_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            try:
                stream = generate_chat_stream(
                    messages=api_messages,
                    provider=current_provider,
                    model_name=active_model,
                    api_key=active_api_key,
                    base_url=active_base_url,
                    response_level=app_cfg["response_level"],
                    use_knowledge=app_cfg["use_knowledge"],
                    graph=st.session_state.graph,
                    temperature=active_temperature,
                    max_tokens=active_max_tokens,
                    system_prompt=active_system_prompt
                )

                for chunk in stream:
                    if hasattr(chunk, "content"):
                        full_response += chunk.content
                        response_placeholder.markdown(full_response + "▌")

                response_placeholder.markdown(full_response)

                st.session_state.messages.append({"role": "assistant", "content": full_response})

                with st.spinner("Extracting knowledge graph..."):

                    text_to_extract = f"User: {prompt}"

                    if app_cfg["graph_source"] == "User Input + Model Response":
                        text_to_extract = f"User: {prompt}\nAssistant: {full_response}"

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


with tab_graph:

    st.subheader("Interactive Knowledge Graph")

    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 1, 1])

    with ctrl_col1:
        with st.popover("Clear Graph Memory & Chat", use_container_width=True):
            st.warning(
                "⚠️ Are you sure? "
                "This will permanently wipe the active "
                "knowledge graph and chat history."
            )
            if st.button("Yes, Clear Everything", type="primary", use_container_width=True):
                st.session_state.graph = initialize_graph()
                save_graph_to_disk(st.session_state.graph)
                st.session_state.messages = []
                st.rerun()

    with ctrl_col2:
        if "graph_view_mode" not in st.session_state:
            st.session_state.graph_view_mode = "3D"
        st.session_state.graph_view_mode = st.radio(
            "View",
            ["3D", "2D"],
            horizontal=True,
            label_visibility="collapsed",
            index=0 if st.session_state.graph_view_mode == "3D" else 1
        )

    with ctrl_col3:
        show_edge_labels = st.checkbox("🏷️ Relationship Labels", value=True)

    if st.session_state.graph_view_mode == "3D":
        render_3d_graph(st.session_state.graph, height=700, show_edge_labels=show_edge_labels)
        st.caption("🖱️ Drag to rotate · Scroll to zoom · Click a node to focus")
    else:
        render_pyvis_graph(st.session_state.graph, height=700)


with tab_memory:

    st.session_state.graph, memory_changed = render_memory_manager(st.session_state.graph)

    if memory_changed:
        save_graph_to_disk(st.session_state.graph)
        st.rerun()


render_footer(
    developer_name="Pooya Chavoshi",
    github_url="https://github.com/pooyaphoenix/CortexKG"
)