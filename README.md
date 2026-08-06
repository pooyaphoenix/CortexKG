# 🧠 CortexKG
### Build a Living Knowledge Graph for Your AI Conversations

> Transform your conversations into a persistent knowledge graph and give LLMs long-term memory based on **your own knowledge**, relationships, and personal context.

---

## Why CortexKG?

Large Language Models are incredibly powerful, but they have one major limitation:

They don't truly **know you**.

Every conversation starts almost from scratch unless you manually provide context or rely on expensive long-context windows.

CortexKG introduces a different approach.

Instead of repeatedly telling the model who you are, what you know, what you've learned, and how everything is connected, CortexKG continuously extracts knowledge from your conversations and stores it as a **graph of entities and relationships**.

Over time, your AI assistant develops something closer to a **digital representation of your mind** rather than simply remembering previous chat history.

---

# The Vision

Imagine owning your own AI memory.

Instead of your personality being trapped inside one chatbot or one vendor, your knowledge becomes portable.

Your ideas.

Your projects.

Your interests.

Your relationships.

Your beliefs.

Your experiences.

Everything becomes part of a structured knowledge graph that can be exported, shared, migrated, visualized, or connected to any future LLM.

CortexKG is an attempt toward giving users ownership over their AI memory instead of locking it inside proprietary systems.

Think of it as creating a lightweight **digital cortex** for yourself.

---

# What CortexKG Does

During every conversation:

1. You chat with your favorite LLM.
2. CortexKG extracts entities and relationships.
3. Those relationships are stored inside a knowledge graph.
4. Future conversations can inject this graph back into the LLM as context.
5. The graph continuously evolves as you learn and communicate.

Instead of only storing text, CortexKG stores **knowledge**.

---

# Features

- 🧠 Persistent personal knowledge graph
- 💬 Chat with multiple LLM providers
- 🌐 Interactive graph visualization
- 🔄 Automatic knowledge extraction
- 📦 Export and import your graph as JSON
- 🔍 Explore relationships between concepts
- 🧩 Provider-independent architecture
- ⚡ Streaming responses
- 🗂 Long-term memory for conversations
- 🔌 Works with local and cloud models

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

# How It Works

```
User
   │
   ▼
Conversation
   │
   ▼
LLM Response
   │
   ▼
Knowledge Extraction
   │
   ▼
Knowledge Graph
   │
   ▼
Context Injection
   │
   ▼
Future Conversations
```

Every conversation strengthens your personal knowledge graph.

---

# Project Architecture

```
                User
                  │
                  ▼
        Streamlit Interface
                  │
      ┌───────────┼───────────┐
      ▼           ▼           ▼
 Chat Engine   Graph Engine  Config Manager
      │           │
      ▼           ▼
 LangChain    NetworkX Graph
      │
      ▼
OpenAI / Gemini / Ollama / Custom APIs
```

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/CortexKG.git

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

---

# Configuration

On first launch, CortexKG creates an `app_config.json` file.

From the sidebar you can configure:

- Model Provider
- Model Name
- API Key
- Base URL
- Response Detail Level
- Graph Extraction Mode
- Knowledge Injection
- Graph Import / Export

No manual editing is required.

---

# Using Ollama

Install Ollama:

https://ollama.com

Pull a model:

```bash
ollama pull gemma3:4b
```

or

```bash
ollama pull llama3
```

Start Ollama and choose:

Provider:

```
Ollama (Local)
```

Base URL:

```
http://localhost:11434
```

No API key is required.

---

# Using OpenAI

Select:

```
OpenAI
```

Provide:

- API Key
- Model name

Example:

```
gpt-4o-mini
```

---

# Using Gemini

Select:

```
Google Gemini
```

Provide:

- Google API Key
- Model name

Example:

```
gemini-1.5-flash
```

---

# Using Custom Providers

Any OpenAI-compatible endpoint can be used.

Examples:

- OpenRouter
- LM Studio
- vLLM
- ArvanCloud
- Local APIs

Simply enter:

- Base URL
- API Key (if required)
- Model Name

---

# Knowledge Graph

CortexKG extracts:

- People
- Places
- Organizations
- Technologies
- Projects
- Ideas
- Skills
- Relationships

Example:

Conversation:

```
I work at OpenAI and I love Python.
```

Extracted graph:

```
me ─────► works_at ─────► OpenAI

me ─────► loves ─────► Python
```

As conversations continue, the graph becomes richer and more interconnected.

---

# Graph Memory

Your graph is automatically saved locally.

You can:

- Export it as JSON
- Import previous graphs
- Merge knowledge over time
- Build your own long-term AI memory

This allows your knowledge to remain yours.

---

# Why a Knowledge Graph?

Traditional chat history looks like this:

```
Message
↓

Message
↓

Message
↓

Message
```

CortexKG stores:

```
Concept
   │
Relationship
   │
Concept
```

Knowledge graphs are:

- searchable
- explainable
- visual
- portable
- expandable

They scale much better than raw chat logs.

---

# Future Ideas

- Vector database integration
- Semantic search
- GraphRAG
- Multi-user knowledge spaces
- Graph analytics
- Automatic ontology refinement
- Temporal relationships
- Memory confidence scoring
- Graph embeddings
- MCP integration
- Local-first encrypted memory
- Multi-agent shared memory

---

# Contributing

Contributions are always welcome.

Whether it's:

- bug fixes
- UI improvements
- new providers
- documentation
- graph algorithms
- memory optimization

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

# Author

**Pooya Chavoshi**

GitHub:
https://github.com/pooyachavoshi

If you find this project useful, consider giving it a ⭐ to support future development.