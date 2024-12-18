# Agentic-Workflows-Playbook

A comprehensive demonstration of various agentic AI workflow frameworks and applications, showcasing different approaches to building autonomous AI systems.

## Overview

This repository contains examples and demonstrations of popular agentic AI frameworks and applications, helping developers understand and implement autonomous AI workflows. Each project showcases different approaches to building intelligent systems that can perform complex tasks autonomously.

## Featured Projects

### 1. Multimodal Chatbot
A powerful AI chatbot that combines image processing, natural language understanding, and multiple specialized tools.
- Key Features:
  - 🖼️ Image processing and OCR
  - 🔍 Multi-source information retrieval (Web, Wikipedia, ArXiv)
  - 📊 Real-time data analysis (Stocks, Weather, News)
  - 🧮 Mathematical computations via Wolfram Alpha
  - 💾 File operations and data processing
  - 🌐 Natural language interface for all operations
- [Learn more](./multimodal_bot/)

### 2. LangGraph Ollama Demo
A demonstration of using LangGraph with Ollama for creating conversational workflows.
- Features:
  - 🔄 Stateful conversation management
  - 🤖 Integration with Ollama's Llama2 model
  - 📝 Short story generation capabilities
  - 🎯 Simple yet effective conversation loop implementation
- [Learn more](./lang_graph/)

### 3. CrewAI Trip Planner
An intelligent travel planning system using multiple specialized AI agents working together.
- Features:
  - 🌍 Smart city selection based on weather, season, and costs
  - 🏛️ Local expertise and cultural insights
  - 📅 Detailed itinerary creation with budget planning
  - 🔍 Multi-source information gathering
  - 🤖 Three specialized agents working in harmony:
    - City Selection Expert
    - Local Expert
    - Travel Concierge
  - 📊 Comprehensive travel plans with day-by-day schedules
- [Learn more](./crewai/)

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Conda (recommended) or virtualenv
- Required API keys (varies by project)
- Ollama with llama3.2 model (for LangGraph and CrewAI demos)

### Quick Start
1. Clone the repository:
```bash
git clone https://github.com/yourusername/Agentic-Workflows-Playbook.git
cd Agentic-Workflows-Playbook
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Choose a project and follow its README for specific setup instructions.

## Repository Structure
```
.
├── multimodal_bot/    # Advanced Multimodal Chatbot
├── lang_graph/        # LangGraph Ollama Demo
├── crewai/           # AI-Powered Trip Planning System
└── docs/             # Documentation and guides
```

## Required API Keys

Different projects may require different API keys:
- OpenAI API Key (for Multimodal Chatbot)
- SERPAPI Key (for enhanced search in Multimodal Chatbot)
- Wolfram Alpha API Key (for mathematical computations)
- Ollama setup with llama3.2 model (for LangGraph and CrewAI)

## Contributing

We welcome contributions! To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please ensure your code follows our style guidelines and includes appropriate documentation.

## License

This project is licensed under the MIT License - see the LICENSE file for details.