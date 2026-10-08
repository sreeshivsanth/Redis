# Redis Agent 🚀

A modular Agentic AI project built with **LangGraph**, **LangChain**, **Groq LLMs**, and **Redis** for stateful session persistence and checkpointing.

---

## 📌 Overview

This project demonstrates two core Agentic AI implementations:

1. **Redis-Backed Stateful Chat Agent (`oyproject.py`)**:
   - Implements persistent conversational memory using `langgraph-checkpoint-redis` (`RedisSaver`).
   - Supports multi-turn conversation threads indexed by `thread_id`, maintaining conversation history across process restarts in Redis.
   - Powered by Groq's fast inference models (`openai/gpt-oss-120b`).

2. **Agentic Student Assistant (`ai.py`)**:
   - An interactive agent equipped with dynamic tool-calling capabilities via LangGraph's `ToolNode` and conditional routing.
   - **Integrated Tools**:
     - 🧮 **Calculator**: Evaluates mathematical expressions safely.
     - 🎓 **Student Information**: Queries student details (name, department).
     - 📊 **Attendance Tracker**: Checks student attendance percentages.
     - 🕒 **Date & Time**: Retrieves current real-time timestamps.

---

## 🛠️ Tech Stack & Dependencies

- **Language**: Python 3.12+
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Frameworks & Libraries**:
  - `langgraph` & `langgraph-checkpoint-redis`
  - `langchain` & `langchain-groq`
  - `groq`
  - `python-dotenv`
- **Database / Cache**: [Redis](https://redis.io/) (for conversational checkpointing)

---

## 📂 Project Structure

```text
├── src/
│   ├── redis/
│   │   └── __init__.py         # Package entry point
│   └── redis_agent/
│       └── __init__.py         # Package module
├── ai.py                       # Agentic AI Student Assistant with custom tools
├── oyproject.py                # Redis-persisted multi-turn chat agent
├── pyproject.toml              # Project dependencies and configurations
├── uv.lock                     # Locked dependency tree
├── .env.example                # Template for environment variables
└── README.md                   # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python `>=3.12`
- [`uv`](https://docs.astral.sh/uv/) installed (or standard `pip` / `venv`)
- Redis instance (running locally or via Docker)
- A [Groq API Key](https://console.groq.com/)

### 2. Clone and Setup Environment

Clone the repository and install the dependencies:

```bash
# Using uv (recommended)
uv sync

# Or using standard pip
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -e .
```

### 3. Environment Configuration

Create a `.env` file in the root directory and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Start Redis (for `oyproject.py`)

If running Redis locally via Docker:

```bash
# Start Redis on port 6380 (as configured by default in oyproject.py)
docker run -d --name redis-agent-db -p 6380:6379 redis:latest
```

> **Note**: If your Redis runs on the default port `6379`, you can update `REDIS_URL` in `oyproject.py`:
> ```python
> REDIS_URL = "redis://localhost:6379"
> ```

---

## 💻 Usage

### Run the Redis-Backed Agent

Run the conversational agent with persistent memory stored in Redis:

```bash
uv run python oyproject.py
```
*Type messages to chat. The session history is automatically saved to Redis under the configured `thread_id` and persists across program executions.*

---

### Run the Agentic Student Assistant

Run the multi-tool assistant in CLI mode:

```bash
uv run python ai.py
```

#### Example Prompts:
- *"What is Arun's attendance and which department is he from?"*
- *"Calculate (15 * 8) / 3 + 20"*
- *"What is the current date and time?"*

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
