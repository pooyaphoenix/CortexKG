import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components
import networkx as nx

def render_pyvis_graph(nx_graph: nx.DiGraph, height: int = 600):
    """Generates HTML file with Pyvis and renders it into Streamlit with full-screen controls."""
    if len(nx_graph.nodes) == 0:
        st.info("The Knowledge Graph is empty. Start chatting to build it!")
        return

    net = Network(notebook=True, width="100%", height=f"{height}px", directed=True)
    net.from_nx(nx_graph)
    
    # Configure physics and enable vis.js navigation buttons (zoom/pan)
    net.set_options("""
    var options = {
      "interaction": {
        "hover": true,
        "navigationButtons": true,
        "keyboard": true
      },
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      }
    }
    """)
    
    html_path = "graph.html"
    net.save_graph(html_path)
    
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Fullscreen script injection with responsive viewport scaling & network redraw
    fullscreen_script = """
    <style>
      .fs-btn {
        position: absolute;
        top: 12px;
        right: 12px;
        z-index: 9999;
        background-color: #1f2937;
        color: #ffffff;
        border: 1px solid #374151;
        padding: 6px 14px;
        border-radius: 6px;
        font-family: sans-serif;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
      }
      .fs-btn:hover { background-color: #374151; }

      /* Force container to 100vh on Fullscreen */
      :fullscreen, :-webkit-full-screen {
        background-color: #ffffff !important;
        width: 100vw !important;
        height: 100vh !important;
        overflow: hidden !important;
      }
      :fullscreen .card, :-webkit-full-screen .card {
        height: 100vh !important;
        width: 100vw !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
      }
      :fullscreen #mynetwork, :-webkit-full-screen #mynetwork {
        height: 100vh !important;
        width: 100vw !important;
        border: none !important;
      }
    </style>
    <button class="fs-btn" onclick="toggleFullScreen()">⛶ Fullscreen</button>
    <script>
    function toggleFullScreen() {
      var elem = document.body;
      if (!document.fullscreenElement && !document.webkitFullscreenElement) {
        if (elem.requestFullscreen) { elem.requestFullscreen(); }
        else if (elem.webkitRequestFullscreen) { elem.webkitRequestFullscreen(); }
        else if (elem.msRequestFullscreen) { elem.msRequestFullscreen(); }
      } else {
        if (document.exitFullscreen) { document.exitFullscreen(); }
        else if (document.webkitExitFullscreen) { document.webkitExitFullscreen(); }
      }
    }

    // Recalculate PyVis canvas dimensions on fullscreen toggle
    document.addEventListener("fullscreenchange", handleResize);
    document.addEventListener("webkitfullscreenchange", handleResize);

    function handleResize() {
      if (typeof network !== 'undefined' && network !== null) {
        setTimeout(function() {
          var isFS = !!(document.fullscreenElement || document.webkitFullscreenElement);
          network.setSize('100%', isFS ? '100vh' : '600px');
          network.redraw();
          network.fit();
        }, 150);
      }
    }
    </script>
    """
    
    if "</body>" in html_content:
        html_content = html_content.replace("</body>", f"{fullscreen_script}</body>")
    else:
        html_content += fullscreen_script

    components.html(html_content, height=height + 25)

def render_footer(developer_name: str = "Pooya Chavoshi", github_url: str = "https://github.com/pooyachavoshi"):
    """Renders a fixed footer at the bottom of the Streamlit application."""
    footer_html = f"""
    <style>
    .app-footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: #808495;
        text-align: center;
        padding: 8px 0;
        font-size: 13px;
        border-top: 1px solid #1f2937;
        z-index: 999;
    }}
    .app-footer a {{
        color: #4da6ff;
        text-decoration: none;
        font-weight: 600;
    }}
    .app-footer a:hover {{
        text-decoration: underline;
    }}
    </style>
    <div class="app-footer">
        Developed by <strong>{developer_name}</strong> | 
        <a href="{github_url}" target="_blank">GitHub Profile</a>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)