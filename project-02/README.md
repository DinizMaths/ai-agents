# 📗 Concepts

## 🕸️ LangGraph

>LangGraph is a library for building stateful, multi-actor applications with LLMs, used to create agent and multi-agent workflows. Compared to other LLM frameworks, it offers these core benefits: cycles, controllability, and persistence. LangGraph allows you to define flows that involve cycles, essential for most agentic architectures, differentiating it from DAG-based solutions. As a very low-level framework, it provides fine-grained control over both the flow and state of your application, crucial for creating reliable agents. Additionally, LangGraph includes built-in persistence, enabling advanced human-in-the-loop and memory features.
>
> [LangChain](https://langchain-ai.github.io/langgraph/)

LangGraph is main based on <b>Nodes</b>, that are functions that change the state and return the state, <b>Edges</b>, that defines the connections and flows between nodes (conditional edges allow for conditional routing), and <b>State</b> that is the data passed and changed from nodes.

# 💻 How to Run
