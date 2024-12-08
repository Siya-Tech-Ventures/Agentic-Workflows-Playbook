# Agentic-Workflows-Playbook

A comprehensive demonstration of various agentic AI workflow frameworks, showcasing different approaches to building autonomous AI systems.

## Overview

This repository contains examples and demonstrations of popular agentic AI frameworks, helping developers understand and implement autonomous AI workflows. Each framework has its own unique approach to creating AI agents that can perform complex tasks autonomously.

## Frameworks Included

### 2. CrewAI
- Framework for orchestrating role-playing AI agents
- Enables creation of specialized agent teams
- Focuses on collaborative problem-solving
- [Examples](./crewai/)

### 3. LangGraph
- Graph-based framework for LLM orchestration
- Enables complex reasoning chains
- Built on top of LangChain
- [Examples](./langgraph/)

### 4. AutoGPT (agpt)
- Autonomous GPT-4 powered agent
- Goal-oriented task completion
- Memory and internet-enabled capabilities
- [Examples](./autogpt/)

### 5. Project Astra
- Experimental framework for autonomous agents
- Focuses on task decomposition and execution
- Supports complex planning capabilities
- [Examples](./astra/)

### 6. OpenAgent
- Open-source framework for building AI agents
- Modular architecture for customization
- Supports multiple LLM backends
- [Examples](./openagent/)

### 7. BabyAGI
- Simple implementation of autonomous agents
- Task creation and prioritization
- Memory management and execution
- [Examples](./babyagi/)

## Setup and Installation

Each framework has its own setup requirements in their respective directories. General requirements:

```bash
python >= 3.9
pip install -r requirements.txt
```

## Repository Structure

```
.
├── autogen/         # AutoGen examples and demos
├── crewai/          # CrewAI implementation
├── langgraph/       # LangGraph demonstrations
├── autogpt/         # AutoGPT examples
├── astra/           # Project Astra implementations
├── openagent/       # OpenAgent demos
├── babyagi/         # BabyAGI examples
└── common/          # Shared utilities and resources
```

## API Keys and Configuration

Most examples require API keys for language models. Create a `.env` file with:

```env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
# Add other API keys as needed
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - feel free to use this code for your own projects.

## Disclaimer

This is a demonstration repository. Some frameworks may require additional setup or have specific requirements. Please refer to each framework's official documentation for production use.