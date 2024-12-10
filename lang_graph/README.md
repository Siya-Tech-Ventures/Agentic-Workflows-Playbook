# LangGraph Ollama Demo

## Overview
This is a simple demonstration of using LangGraph with Ollama as the language model. The demo creates a conversational graph that generates a short story.

## Project Structure
```
lang_graph/
├── langgraph_ollama_demo.py
├── requirements.txt
├── environment.yml
└── README.md
```

## Prerequisites
- Conda (Anaconda or Miniconda) or Python 3.9+
- Ollama installed and running
- Llama3.2 model pulled (`ollama pull llama3.2`)

## Setup

### Option 1: Conda Environment (Recommended)

1. Create the Conda environment:
```bash
conda env create -f environment.yml
```

2. Activate the environment:
```bash
conda activate langgraph-ollama
```

3. Run the demo:
```bash
python langgraph_ollama_demo.py
```

### Option 2: Virtual Environment

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the demo:
```bash
python langgraph_ollama_demo.py
```

## How it Works
- Uses LangGraph to create a stateful conversation workflow
- Utilizes Ollama's Llama2 model for generating responses
- Implements a simple conversation loop with a maximum of 3 exchanges

## Key Components
- `GraphState`: Defines the conversation state
- `generate_response()`: Generates AI responses
- `route_to_end()`: Determines conversation termination

## Notes
- Ensure Ollama is running before executing the script
- The demo generates a short story based on an initial prompt

## Troubleshooting
- If you encounter any dependency issues, ensure you're using Python 3.9+
- Verify that Ollama is installed and the Llama2 model is pulled
- Check that all dependencies are correctly installed in your environment

## Dependencies
- LangChain: 0.2.0
- LangGraph: 0.2.54
- Ollama: 0.1.3
- Pydantic: 2.6.1
