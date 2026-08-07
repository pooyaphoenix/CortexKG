<p align="center">
<img width="468" height="190" alt="RA3G-logo" src="https://github.com/user-attachments/assets/60e2bf53-e417-4bcb-ae48-12ef268b20da" />
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

## Why CortexKG?

Large Language Models are incredibly powerful, but they have one major limitation:

They don't truly **know you**.

Every conversation starts almost from scratch unless you manually provide context or rely on expensive long-context windows.

CortexKG introduces a different approach.

Instead of repeatedly telling the model who you are, what you know, what you've learned, and how everything is connected, CortexKG continuously extracts knowledge from your conversations and stores it as a **graph of entities and relationships**.

Over time, your AI assistant develops something closer to a **digital representation of your mind** rather than simply remembering previous chat history.

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


# 🤝Contributing

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