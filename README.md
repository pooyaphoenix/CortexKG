<p align="center">
   <img width="800" height="500" alt="CortexKG" src="https://github.com/user-attachments/assets/2a57efda-9239-4052-8e35-a2cbdff16a5d" />
</p>

<p align="center">
   <b>CortexKG: Portable AI memory powered by knowledge graphs</b>
</p>

<p align="center">
  <a href="https://github.com/pooyaphoenix/CortexKG/releases">
    <img src="https://img.shields.io/github/v/release/pooyaphoenix/CortexKG?color=blue&label=version" alt="Release Version"/>
  </a>
  <a href="https://github.com/pooyaphoenix/CortexKG/stargazers">
    <img src="https://img.shields.io/github/stars/pooyaphoenix/CortexKG?style=social" alt="GitHub stars"/>
  </a>
  <a href="mailto:pooyachavoshi@gmail.com">
    <img src="https://img.shields.io/badge/Email-Contact-blue?style=flat&logo=gmail" alt="Email"/>
  </a>
</p>

# 🧠 CortexKG
### Build a Living Knowledge Graph for Your AI Conversations

> Transform your conversations into a persistent knowledge graph and give LLMs long-term memory based on **your own knowledge**, relationships, and personal context.

---
> **Persian Documentation:** [مطالعه مستندات فارسی](README.fa.md)
## Why CortexKG?

https://github.com/user-attachments/assets/1029c9cf-2a2a-4a6d-9700-3730d4d936fb

Large Language Models are incredibly powerful, but they have one major limitation:

They don't truly **know you**.

Every conversation starts almost from scratch unless you manually provide context or rely on expensive long-context windows.

CortexKG introduces a different approach.

Instead of repeatedly telling the model who you are, what you know, what you've learned, and how everything is connected, CortexKG continuously extracts knowledge from your conversations and stores it as a **graph of entities and relationships**.

Over time, your AI assistant develops something closer to a **digital representation of your mind** rather than simply remembering previous chat history.

---


# What CortexKG Does
<img width="800" height="400" alt="Screenshot 2026-08-07 213124" src="https://github.com/user-attachments/assets/5e0f2078-f824-4218-b5a7-7226f0d477b5" />

During every conversation:

1. You chat with your favorite LLM.
2. CortexKG extracts entities and relationships.
3. Those relationships are stored inside a knowledge graph — **with a timestamp recording exactly when each piece of knowledge was learned**.
4. You can inspect, explore, and manage your stored memories.
5. Future conversations can inject this graph back into the LLM as context.
6. The graph continuously evolves as you learn and communicate.

Instead of only storing text, CortexKG stores **knowledge** — and remembers *when* it learned it.

---

# ✨ Features

### Memory & Knowledge
- 🧠 **Persistent AI Memory** — Store knowledge from conversations as a living knowledge graph.
- ⏱️ **Temporal Memory** — Every entity and relationship is timestamped with when it was first learned and last mentioned.
- 🗂️ **Memory Control Center** — Search, filter, sort, edit, confirm, reject, and delete memories.
- ✅ **Memory Review** — Mark extracted memories as confirmed, unreviewed, or rejected.
- 🔄 **Portable Memory** — Export and import your knowledge graph as JSON.
- 🧩 **Graph-Based Context** — Use stored knowledge as context for future LLM conversations.

### Visualization
- 🌐 **3D Knowledge Graph Explorer** — Orbit, zoom, and fly through your knowledge in three dimensions.
- 🏷️ **Always-Visible Labels** — Entity and relationship names render directly in the scene, no hovering required.
- ⏳ **Timeline Scrubber & Playback** — Rewind your graph to any point in time and watch it grow chronologically.
- 🎨 **Dual Color Modes** — Color nodes by review status or by age.
- 📊 **Knowledge Timeline Panel** — Chart of new entities learned per day, plus a full chronological log.
- 🔀 **2D / 3D Toggle** — Switch back to the classic 2D view anytime.

### Models & Control
- 💬 **Multi-Provider LLM Support** — Ollama, OpenAI, Gemini, and OpenAI-compatible APIs.
- 🌡️ **Per-Provider Generation Settings** — Independent temperature and max token limits for each provider.
- 📝 **Custom System Prompt** — Define your own system instruction, or fall back to built-in detail levels.
- 🔒 **Local-First Support** — Use Ollama for local inference and local memory storage.

---

# 🌐 3D Knowledge Graph Explorer

Your knowledge graph is rendered as an interactive 3D force-directed graph using **Three.js / WebGL**, giving dense clusters room to separate in a way flat 2D layouts can't.

**Exploration controls:**

| Action | Control |
|---|---|
| Rotate | Drag |
| Zoom | Scroll |
| Pan | Right-drag |
| Focus an entity | Click a node — the camera flies to it |
| Reset camera | 🎯 Reset View |
| Expand | ⛶ Fullscreen |

**Visual encoding:**

- **Node color** — review status (✅ confirmed / 🟡 unreviewed / ❌ rejected), switchable to age-based coloring
- **Node size** — number of connections, so hub entities stand out immediately
- **Directional arrows and flowing particles** — relationship direction at a glance
- **Floating labels** — entity names and relationship types always readable

Prefer the flat view for very dense graphs? The 2D renderer is one toggle away.

---

# ⏳ Temporal Memory

Knowing *what* your AI remembers is useful. Knowing *when* it learned it is what makes that memory auditable.

Every node and edge in the graph carries:

- **`created_at`** — when this knowledge first entered the graph
- **`updated_at`** — the most recent conversation that mentioned it
- **`mention_count`** — how many times it has come up

### Time-Travel Scrubber

The 3D view includes a timeline control at the bottom of the canvas. Drag the slider to rewind the graph to any moment in its history, or press **▶** to watch your knowledge assemble itself chronologically from the first entity to the most recent.

Rather than rebuilding the layout on every frame, the scrubber toggles node visibility — so the graph stays spatially stable while entities fade in over time.

### Knowledge Timeline Panel

Below the graph, an expandable timeline panel shows:

- A bar chart of how many new entities you learned per day
- A full chronological log with first-seen, last-mentioned, and mention counts for every entity

> **Note on existing graphs:** knowledge captured before this feature was added is honestly labelled `unknown` rather than backfilled with a fabricated date. Those entries remain permanently visible on the timeline scrubber.

---

# 🧠 Memory Management

CortexKG gives you direct control over what your AI remembers.
<img width="800" height="390" alt="VideoProject7-ezgif com-crop" src="https://github.com/user-attachments/assets/c8b46c63-f05f-480e-b08f-97c9ec5c586b" />



From the **Memory Control Center**, you can:

- 🔎 Search and filter memories
- 🔃 Sort by recently updated, recently created, most mentioned, or name
- ✏️ Edit memory labels and entity types
- ✅ Confirm memories
- ❌ Reject memories
- 🗑️ Delete memories
- 🔗 Inspect relationships, including when each was first seen
- 📅 See when each memory was first learned and last mentioned
- 📊 View memory statistics

This makes CortexKG's memory **transparent, editable, and user-controlled**.

---

# ⚙️ Configuration

All settings live in the sidebar and persist to `app_config.json` automatically — no restart required.

### 🤖 Model & Connection
Always visible. Pick your provider, model name, and connection details.

| Setting | Description |
|---|---|
| LLM Provider | Ollama, OpenAI, Google Gemini, or a custom OpenAI-compatible endpoint |
| Model Name | Per-provider model identifier |
| Base URL | For Ollama and custom endpoints |
| API Key | Stored per provider, so you can switch without re-entering keys |

### 🎛️ Generation & Prompt

| Setting | Description |
|---|---|
| Temperature | `0.0` – `2.0`, stored per provider. One-click presets: 🎯 Precise · ⚖️ Balanced · 🎨 Creative |
| Max Tokens | Response length cap, mapped to each backend's native parameter |
| Response Detail Level | Short / Medium / Long built-in instructions |
| Custom System Prompt | Your own instruction — overrides Response Detail Level when filled in |

Max tokens is translated correctly for each backend: `max_tokens` for OpenAI-compatible APIs, `max_output_tokens` for Gemini, and `num_predict` for Ollama.

### 🧠 Knowledge Graph Behavior

| Setting | Description |
|---|---|
| Use Graph as Knowledge Context | Inject stored entities and relationships into the system prompt |
| Build Graph From | Extract from user input only, or user input plus model responses |

### 💾 Data & Memory
Export your graph as JSON, import a previous export, or reset all settings to defaults.

---

# Supported Providers

Currently CortexKG supports:

- Ollama (Local)
- OpenAI
- Google Gemini
- Any OpenAI-compatible API

Examples include:

- OpenRouter
- LM Studio
- vLLM
- ArvanCloud
- Local OpenAI-compatible servers

---

# 🚀Installation
## 1. 🐳 Run with Docker (Recommended)

```bash
git clone https://github.com/pooyaphoenix/CortexKG.git
cd CortexKG
docker compose up -d
```

Open **http://localhost:8501**. Settings, API keys, and your knowledge graph all
persist in a Docker volume across restarts.

> **Using Ollama?** From inside the container, `localhost` refers to the
> container itself. Set the Ollama Base URL in Settings to
> `http://host.docker.internal:11434` to reach an Ollama instance running on
> your host machine — or uncomment the optional `ollama` service in
> `docker-compose.yml` to run it fully containerized instead.

## 2. Clone the repository

```bash
git clone https://github.com/pooyaphoenix/CortexKG.git

cd CortexKG
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the application

```bash
python main.py
```

The application will automatically launch Streamlit.

> The 3D graph renderer loads client-side from a CDN, so it adds **no Python dependencies** to your environment.

---

# 🤝Contributing

Contributions are always welcome.

Whether it's:

- bug fixes
- UI improvements
- new providers
- documentation
- graph algorithms
- memory optimization
- entity resolution and deduplication

Feel free to open an issue or submit a pull request.

---

# Philosophy

CortexKG is built around one simple idea:

> Your knowledge should belong to you.

AI systems should remember what **you choose**, understand how your ideas connect, and allow you to carry that memory between different models and providers.

Your memory shouldn't disappear when you switch from GPT to Gemini, from Claude to Ollama, or from one platform to another.

CortexKG aims to make personal AI memory portable, transparent, and owned by the user.

---

# License

This project is licensed under the MIT License.

---

Email:
pooyachavoshi@gmail.com

If you find this project useful, consider giving it a ⭐ to support future development.
