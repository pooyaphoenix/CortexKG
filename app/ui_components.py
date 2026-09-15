import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components
import networkx as nx
import json

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

def render_3d_graph(nx_graph: nx.DiGraph, height: int = 700, show_edge_labels: bool = True):
    """Renders the knowledge graph in 3D with always-on labels and a time-travel scrubber."""
    from time_service import ensure_timestamps, to_epoch_ms, format_timestamp

    if len(nx_graph.nodes) == 0:
        st.info("The Knowledge Graph is empty. Start chatting to build it!")
        return

    ensure_timestamps(nx_graph)

    status_colors = {
        "confirmed": "#22c55e",
        "unreviewed": "#eab308",
        "rejected": "#ef4444",
    }

    nodes_json = []
    node_ms = {}
    for node_id, data in nx_graph.nodes(data=True):
        status = data.get("status", "unreviewed")
        ms = to_epoch_ms(data.get("created_at"))
        node_ms[node_id] = ms
        nodes_json.append({
            "id": str(node_id),
            "label": str(data.get("label", node_id)),
            "entity_type": str(data.get("entity_type", "unknown")),
            "status": status,
            "color": status_colors.get(status, "#60a5fa"),
            "degree": nx_graph.degree(node_id),
            "ts": ms,
            "created": format_timestamp(data.get("created_at")),
            "updated": format_timestamp(data.get("updated_at")),
            "mentions": int(data.get("mention_count") or 0),
        })

    links_json = []
    for source, target, data in nx_graph.edges(data=True):
        # A link can only appear once both its endpoints exist, so its effective
        # timeline position is the latest of (edge, source node, target node).
        candidates = [
            v for v in (to_epoch_ms(data.get("created_at")), node_ms.get(source), node_ms.get(target))
            if v is not None
        ]
        links_json.append({
            "source": str(source),
            "target": str(target),
            "relation": data.get("label", "RELATED_TO"),
            "ts": max(candidates) if candidates else None,
            "created": format_timestamp(data.get("created_at")),
        })

    graph_data_json = json.dumps({"nodes": nodes_json, "links": links_json})

    html_template = """
    <div id="graph3d-wrap" style="width:100%; height:__H__px; position:relative; background:#0e1117; border-radius:8px; overflow:hidden;">
        <button class="g3d-btn g3d-fs" onclick="g3dToggleFullscreen()">⛶ Fullscreen</button>
        <button class="g3d-btn g3d-reset" onclick="g3dResetCamera()">🎯 Reset View</button>
        <div class="g3d-legend">
            <span><i style="background:#22c55e;"></i> Confirmed</span>
            <span><i style="background:#eab308;"></i> Unreviewed</span>
            <span><i style="background:#ef4444;"></i> Rejected</span>
        </div>
        <div class="g3d-count" id="g3d-count"></div>
        <div class="g3d-timeline" id="g3d-timeline" style="display:none;">
            <button class="g3d-tl-btn" id="g3d-play">▶</button>
            <input type="range" id="g3d-slider" min="0" max="1000" value="1000">
            <span class="g3d-tl-label" id="g3d-time"></span>
            <button class="g3d-tl-btn g3d-tl-mode" id="g3d-mode">🎨 Status</button>
        </div>
        <div id="g3d-canvas"></div>
    </div>

    <style>
        .g3d-btn {
            position: absolute; top: 12px; z-index: 9999;
            background-color: #1f2937; color: #fff; border: 1px solid #374151;
            padding: 6px 14px; border-radius: 6px; font-family: sans-serif;
            font-size: 13px; font-weight: 600; cursor: pointer;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        }
        .g3d-btn:hover { background-color: #374151; }
        .g3d-fs { right: 12px; }
        .g3d-reset { right: 140px; }
        .g3d-legend {
            position: absolute; top: 12px; left: 12px; z-index: 9999;
            background-color: rgba(31,41,55,0.85); padding: 6px 10px; border-radius: 6px;
            font-family: sans-serif; font-size: 12px; color: #d1d5db; display: flex; gap: 10px;
        }
        .g3d-legend i { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; }
        .g3d-count {
            position: absolute; top: 48px; left: 12px; z-index: 9999;
            color: #9ca3af; font-family: sans-serif; font-size: 12px;
            background-color: rgba(31,41,55,0.7); padding: 4px 10px; border-radius: 6px;
        }
        .g3d-timeline {
            position: absolute; bottom: 14px; left: 50%; transform: translateX(-50%);
            z-index: 9999; width: min(80%, 720px);
            background-color: rgba(31,41,55,0.9); border: 1px solid #374151;
            padding: 8px 12px; border-radius: 8px;
            display: flex; align-items: center; gap: 10px;
            font-family: sans-serif; box-shadow: 0 2px 10px rgba(0,0,0,0.4);
        }
        .g3d-tl-btn {
            background-color: #374151; color: #fff; border: none;
            padding: 4px 10px; border-radius: 5px; cursor: pointer;
            font-size: 13px; font-weight: 600; white-space: nowrap;
        }
        .g3d-tl-btn:hover { background-color: #4b5563; }
        .g3d-tl-mode { font-size: 12px; }
        #g3d-slider { flex: 1; accent-color: #60a5fa; cursor: pointer; }
        .g3d-tl-label {
            color: #d1d5db; font-size: 12px; min-width: 112px; text-align: center; white-space: nowrap;
        }
        :fullscreen #graph3d-wrap, :-webkit-full-screen #graph3d-wrap {
            width: 100vw !important; height: 100vh !important; border-radius: 0 !important;
        }
    </style>

    <script type="module">
        import ForceGraph3D from "https://esm.sh/3d-force-graph";
        import SpriteText from "https://esm.sh/three-spritetext";

        const graphData = __DATA__;
        const showEdgeLabels = __EDGE_LABELS__;
        const elem = document.getElementById('g3d-canvas');

        // ---- Timeline bounds -------------------------------------------------
        const stamps = graphData.nodes.map(n => n.ts).filter(v => v !== null);
        const minTs = stamps.length ? stamps.reduce((a, b) => Math.min(a, b)) : 0;
        const maxTs = stamps.length ? stamps.reduce((a, b) => Math.max(a, b)) : 0;
        const hasTimeline = stamps.length > 0 && maxTs > minTs;
        let cursor = maxTs;
        let colorMode = 'status';

        function ageColor(n) {
            if (n.ts === null) return '#475569';
            const t = maxTs === minTs ? 1 : (n.ts - minTs) / (maxTs - minTs);
            // oldest = cool blue, newest = warm amber
            const r = Math.round(59 + t * (251 - 59));
            const g = Math.round(130 + t * (191 - 130));
            const b = Math.round(246 + t * (36 - 246));
            return 'rgb(' + r + ',' + g + ',' + b + ')';
        }

        const Graph = new ForceGraph3D(elem)
            .graphData(graphData)
            .backgroundColor('#0e1117')
            .nodeColor(n => colorMode === 'status' ? n.color : ageColor(n))
            .nodeVal(n => Math.max(2, Math.sqrt(n.degree + 1) * 3))
            .nodeOpacity(0.95)
            .nodeLabel(n => `<div style="font-family:sans-serif;padding:4px;">
                                <b>${n.label}</b><br/>
                                <span style="color:#9ca3af;">${n.entity_type} · ${n.status}</span><br/>
                                <span style="color:#9ca3af;">First seen: ${n.created}</span><br/>
                                <span style="color:#9ca3af;">Last mentioned: ${n.updated} (${n.mentions}x)</span>
                             </div>`)
            .nodeThreeObjectExtend(true)
            .nodeThreeObject(node => {
                const sprite = new SpriteText(node.label);
                sprite.material.depthWrite = false;
                sprite.color = node.color;
                sprite.textHeight = 3.2;
                sprite.center.y = -0.9;
                return sprite;
            })
            .linkColor(() => 'rgba(148,163,184,0.55)')
            .linkLabel(l => `${l.relation} · ${l.created}`)
            .linkDirectionalArrowLength(4)
            .linkDirectionalArrowRelPos(1)
            .linkDirectionalParticles(1)
            .linkDirectionalParticleWidth(1.5)
            .linkDirectionalParticleSpeed(0.006)
            .linkWidth(1)
            .width(elem.parentElement.clientWidth)
            .height(__H__)
            .onNodeClick(node => {
                const distance = 80;
                const distRatio = 1 + distance / Math.hypot(node.x, node.y, node.z);
                Graph.cameraPosition(
                    { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio },
                    node,
                    1000
                );
            })
            .onNodeHover(node => { elem.style.cursor = node ? 'pointer' : 'default'; });

        if (showEdgeLabels) {
            Graph.linkThreeObjectExtend(true)
                .linkThreeObject(link => {
                    const sprite = new SpriteText(link.relation);
                    sprite.color = 'lightgrey';
                    sprite.textHeight = 2.2;
                    return sprite;
                })
                .linkPositionUpdate((sprite, { start, end }) => {
                    const middlePos = Object.assign(...['x', 'y', 'z'].map(c => ({
                        [c]: start[c] + (end[c] - start[c]) / 2
                    })));
                    Object.assign(sprite.position, middlePos);
                });
        }

        // ---- Visibility filtering (keeps layout stable, unlike re-setting graphData) ----
        const countEl = document.getElementById('g3d-count');
        const timeEl = document.getElementById('g3d-time');

        function visibleNode(n) { return n.ts === null || n.ts <= cursor; }
        function visibleLink(l) { return l.ts === null || l.ts <= cursor; }

        function applyFilter() {
            Graph.nodeVisibility(visibleNode).linkVisibility(visibleLink);
            const nv = graphData.nodes.filter(visibleNode).length;
            const lv = graphData.links.filter(visibleLink).length;
            countEl.innerText = nv + ' / ' + graphData.nodes.length + ' entities · '
                              + lv + ' / ' + graphData.links.length + ' relationships';
            if (hasTimeline) {
                timeEl.innerText = new Date(cursor).toLocaleString(undefined, {
                    year: 'numeric', month: 'short', day: 'numeric',
                    hour: '2-digit', minute: '2-digit'
                });
            }
        }

        if (hasTimeline) {
            document.getElementById('g3d-timeline').style.display = 'flex';

            const slider = document.getElementById('g3d-slider');
            const playBtn = document.getElementById('g3d-play');
            const modeBtn = document.getElementById('g3d-mode');
            let playing = false;
            let timer = null;

            slider.addEventListener('input', () => {
                cursor = minTs + (maxTs - minTs) * (slider.value / 1000);
                applyFilter();
            });

            function stop() {
                playing = false;
                playBtn.innerText = '▶';
                if (timer) { clearInterval(timer); timer = null; }
            }

            playBtn.addEventListener('click', () => {
                if (playing) { stop(); return; }
                playing = true;
                playBtn.innerText = '⏸';
                if (Number(slider.value) >= 1000) { slider.value = 0; }
                timer = setInterval(() => {
                    let v = Number(slider.value) + 12;
                    if (v >= 1000) { v = 1000; stop(); }
                    slider.value = v;
                    cursor = minTs + (maxTs - minTs) * (v / 1000);
                    applyFilter();
                }, 60);
            });

            modeBtn.addEventListener('click', () => {
                colorMode = (colorMode === 'status') ? 'age' : 'status';
                modeBtn.innerText = (colorMode === 'status') ? '🎨 Status' : '🕰️ Age';
                Graph.nodeColor(n => colorMode === 'status' ? n.color : ageColor(n));
            });
        }

        applyFilter();

        // ---- Camera / view helpers ------------------------------------------
        let autoRotate = true;
        Graph.controls().addEventListener('start', () => { autoRotate = false; });

        (function spin() {
            if (autoRotate) { Graph.scene().rotation.y += 0.0015; }
            requestAnimationFrame(spin);
        })();

        window.g3dToggleFullscreen = function() {
            const c = document.getElementById('graph3d-wrap');
            if (!document.fullscreenElement && !document.webkitFullscreenElement) {
                (c.requestFullscreen || c.webkitRequestFullscreen).call(c);
            } else {
                (document.exitFullscreen || document.webkitExitFullscreen).call(document);
            }
        };

        document.addEventListener('fullscreenchange', g3dResize);
        document.addEventListener('webkitfullscreenchange', g3dResize);

        function g3dResize() {
            setTimeout(() => {
                const isFS = !!(document.fullscreenElement || document.webkitFullscreenElement);
                Graph.width(isFS ? window.innerWidth : elem.parentElement.clientWidth);
                Graph.height(isFS ? window.innerHeight : __H__);
            }, 150);
        }

        window.g3dResetCamera = function() {
            Graph.cameraPosition({ x: 0, y: 0, z: 300 }, { x: 0, y: 0, z: 0 }, 1000);
            autoRotate = true;
        };
    </script>
    """

    html_content = (
        html_template
        .replace("__DATA__", graph_data_json)
        .replace("__EDGE_LABELS__", "true" if show_edge_labels else "false")
        .replace("__H__", str(height))
    )
    components.html(html_content, height=height + 40)

def render_timeline_panel(nx_graph):
    """Chronological view of when knowledge entered the graph."""
    import pandas as pd
    from time_service import get_timeline_events, get_daily_counts

    if len(nx_graph.nodes) == 0:
        return

    events = get_timeline_events(nx_graph)
    daily = get_daily_counts(nx_graph)

    st.markdown("#### 📅 Knowledge Timeline")

    if daily:
        st.caption("New entities learned per day")
        chart_df = pd.DataFrame(
            {"Entities learned": list(daily.values())},
            index=list(daily.keys())
        )
        st.bar_chart(chart_df)
    else:
        st.info(
            "No dated entities yet. Knowledge captured before this feature was added "
            "shows as 'unknown' — new entries from now on will be timestamped."
        )

    st.caption("Chronological log (newest first)")
    st.dataframe(events, use_container_width=True, hide_index=True)

def render_memory_manager(nx_graph):
    """
    Interactive memory management interface.

    Returns:
        (graph, changed)
    """

    import streamlit as st
    from graph_service import (
        get_memory_stats,
        get_memory_nodes,
        update_memory_node,
        set_memory_status,
        delete_memory,
        ensure_memory_metadata,
    )
    from time_service import (
        ensure_timestamps,
        format_timestamp,
        relative_time,
    )

    ensure_memory_metadata(nx_graph)
    ensure_timestamps(nx_graph)

    changed = False

    st.subheader("🧠 Memory Management")
    st.caption(
        "Inspect, edit, confirm, reject, and delete the knowledge CortexKG remembers."
    )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    stats = get_memory_stats(nx_graph)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Memories", stats["nodes"])
    col2.metric("Relationships", stats["edges"])
    col3.metric("✅ Confirmed", stats["confirmed"])
    col4.metric("🟡 Unreviewed", stats["unreviewed"])
    col5.metric("❌ Rejected", stats["rejected"])

    st.divider()

    # ---------------------------------------------------------
    # Filters & Sorting
    # ---------------------------------------------------------

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([2, 1, 1, 1])

    with filter_col1:
        search = st.text_input(
            "🔎 Search memories",
            placeholder="Search by entity name..."
        )

    entity_types = sorted(
        set(
            str(data.get("entity_type", "unknown"))
            for _, data in nx_graph.nodes(data=True)
        )
    )

    with filter_col2:
        entity_type = st.selectbox(
            "Entity Type",
            ["All"] + entity_types
        )

    with filter_col3:
        status = st.selectbox(
            "Status",
            [
                "All",
                "confirmed",
                "unreviewed",
                "rejected"
            ]
        )

    with filter_col4:
        sort_choice = st.selectbox(
            "Sort by",
            [
                "Recently updated",
                "Recently created",
                "Most mentioned",
                "Name (A–Z)"
            ]
        )

    # ---------------------------------------------------------
    # Memory list
    # ---------------------------------------------------------

    memories = get_memory_nodes(
        nx_graph,
        search=search,
        entity_type=entity_type,
        status=status
    )

    st.caption(f"{len(memories)} memories found")

    if not memories:
        st.info("No memories match the current filters.")
        return nx_graph, changed

    # Apply the chosen ordering. Entries with no timestamp (captured before
    # time tracking existed) sort to the bottom via the "" fallback.
    if sort_choice == "Recently updated":
        memories.sort(
            key=lambda m: nx_graph.nodes[m["id"]].get("updated_at") or "",
            reverse=True
        )
    elif sort_choice == "Recently created":
        memories.sort(
            key=lambda m: nx_graph.nodes[m["id"]].get("created_at") or "",
            reverse=True
        )
    elif sort_choice == "Most mentioned":
        memories.sort(
            key=lambda m: int(nx_graph.nodes[m["id"]].get("mention_count") or 0),
            reverse=True
        )
    else:
        memories.sort(key=lambda m: str(m["label"]).lower())

    memory_options = {}

    for memory in memories:

        status_icon = {
            "confirmed": "✅",
            "unreviewed": "🟡",
            "rejected": "❌",
        }.get(memory["status"], "⚪")

        node_meta = nx_graph.nodes[memory["id"]]

        display = (
            f"{status_icon} "
            f"{memory['label']} "
            f"· {memory['entity_type']} "
            f"· {memory['degree']} connections "
            f"· {relative_time(node_meta.get('updated_at'))}"
        )

        memory_options[display] = memory["id"]

    selected_display = st.selectbox(
        "Select a memory",
        list(memory_options.keys())
    )

    selected_id = memory_options[selected_display]

    node_data = nx_graph.nodes[selected_id]

    st.divider()

    # ---------------------------------------------------------
    # Selected memory
    # ---------------------------------------------------------

    detail_col1, detail_col2 = st.columns([1, 1])

    with detail_col1:

        st.markdown("### Memory")

        with st.form(f"edit_memory_{selected_id}"):

            edited_label = st.text_input(
                "Label",
                value=node_data.get(
                    "label",
                    selected_id
                )
            )

            edited_type = st.text_input(
                "Entity Type",
                value=node_data.get(
                    "entity_type",
                    "unknown"
                )
            )

            current_status = node_data.get(
                "status",
                "unreviewed"
            )

            st.text_input(
                "Memory ID",
                value=str(selected_id),
                disabled=True
            )

            st.text_input(
                "Current Status",
                value=current_status,
                disabled=True
            )

            st.text_input(
                "First Seen",
                value=format_timestamp(
                    node_data.get("created_at")
                ),
                disabled=True
            )

            st.text_input(
                "Last Mentioned",
                value=(
                    f"{format_timestamp(node_data.get('updated_at'))} "
                    f"({int(node_data.get('mention_count') or 0)} mentions)"
                ),
                disabled=True
            )

            save_button = st.form_submit_button(
                "💾 Save Changes",
                use_container_width=True
            )

            if save_button:

                if not edited_label.strip():
                    st.error("Memory label cannot be empty.")

                else:

                    update_memory_node(
                        nx_graph,
                        selected_id,
                        edited_label,
                        edited_type
                    )

                    changed = True

                    st.success(
                        "Memory updated successfully."
                    )

    with detail_col2:

        st.markdown("### Memory Actions")

        current_status = node_data.get(
            "status",
            "unreviewed"
        )

        if current_status != "confirmed":

            if st.button(
                "✅ Confirm Memory",
                use_container_width=True
            ):

                set_memory_status(
                    nx_graph,
                    selected_id,
                    "confirmed"
                )

                changed = True

                st.success(
                    "Memory confirmed."
                )

        if current_status != "rejected":

            if st.button(
                "❌ Reject Memory",
                use_container_width=True
            ):

                set_memory_status(
                    nx_graph,
                    selected_id,
                    "rejected"
                )

                changed = True

                st.warning(
                    "Memory marked as rejected."
                )

        if current_status != "unreviewed":

            if st.button(
                "↩️ Reset Review Status",
                use_container_width=True
            ):

                set_memory_status(
                    nx_graph,
                    selected_id,
                    "unreviewed"
                )

                changed = True

        st.divider()

        st.markdown("### Danger Zone")

        delete_confirm = st.checkbox(
            "I understand this memory and its relationships will be deleted."
        )

        if st.button(
            "🗑️ Delete Memory",
            type="primary",
            use_container_width=True,
            disabled=not delete_confirm
        ):

            delete_memory(
                nx_graph,
                selected_id
            )

            changed = True

            st.success(
                f"Deleted memory: {selected_id}"
            )

            st.rerun()

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    st.divider()

    st.markdown("### 🔗 Relationships")

    incoming = []

    for source, _, data in nx_graph.in_edges(
        selected_id,
        data=True
    ):

        source_data = nx_graph.nodes[source]

        incoming.append(
            {
                "Direction": "← Incoming",
                "Entity": source_data.get(
                    "label",
                    source
                ),
                "Relation": data.get(
                    "label",
                    "RELATED_TO"
                ),
                "First Seen": format_timestamp(
                    data.get("created_at")
                ),
                "Mentions": int(
                    data.get("mention_count") or 0
                )
            }
        )

    outgoing = []

    for _, target, data in nx_graph.out_edges(
        selected_id,
        data=True
    ):

        target_data = nx_graph.nodes[target]

        outgoing.append(
            {
                "Direction": "Outgoing →",
                "Entity": target_data.get(
                    "label",
                    target
                ),
                "Relation": data.get(
                    "label",
                    "RELATED_TO"
                ),
                "First Seen": format_timestamp(
                    data.get("created_at")
                ),
                "Mentions": int(
                    data.get("mention_count") or 0
                )
            }
        )

    relationships = incoming + outgoing

    if relationships:
        st.dataframe(
            relationships,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info(
            "This memory currently has no relationships."
        )

    return nx_graph, changed

def render_footer(developer_name: str = "Pooya Chavoshi", github_url: str = "https://github.com/pooyaphoenix"):
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
        <a href="{github_url}" target="_blank">GitHub Profile</a>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)