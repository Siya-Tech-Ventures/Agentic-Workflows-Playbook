# CrewAI Demo: Multi-Agent Task Orchestration

A demonstration of using CrewAI framework to create and orchestrate multiple AI agents working together to accomplish complex tasks. This demo features a sophisticated trip planning system that leverages multiple specialized agents to create personalized travel itineraries.

## Overview

This project showcases how to use CrewAI to create a team of specialized AI agents that can collaborate effectively to solve problems. The implementation focuses on a travel planning system where different agents work together to select destinations, provide local expertise, and create detailed itineraries.

## 🌟 Key Features

- 🤖 Multi-agent collaboration system
- 🎭 Role-based agent specialization
- 📋 Task delegation and management
- 🔄 Sequential and parallel task execution
- 🧠 Shared knowledge management
- 🌍 Intelligent trip planning capabilities

## 🛠️ Components

### 1. Agent Roles (`trip_agents.py`)
- **City Selection Expert**: Analyzes and selects the best city based on weather, season, and prices
- **Local Expert**: Provides detailed insights about the selected city
- **Travel Concierge**: Creates comprehensive travel itineraries with budget and packing suggestions

### 2. Task Types (`trip_tasks.py`)
- **City Identification**: Analyzes and selects the optimal city based on criteria
- **Local Information Gathering**: Compiles in-depth city guides
- **Trip Planning**: Creates detailed day-by-day itineraries
- Each task includes specific goals and expected outputs

### 3. Main Application (`main.py`)
- Interactive command-line interface
- Orchestrates the collaboration between agents
- Handles user input for:
  - Origin location
  - Potential destination cities
  - Travel date range
  - Personal interests

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Ollama with llama3.2 model
- Required Python packages

### Installation

1. Create and activate a virtual environment:
```bash
# Using conda (recommended)
conda create -n crewai-demo python=3.9
conda activate crewai-demo

# OR using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add necessary configurations
```

### Running the Trip Planner

1. Start the application:
```bash
python main.py
```

2. Follow the prompts to input:
- Your departure location
- Potential destination cities
- Travel date range
- Your interests and hobbies

## 📁 Project Structure
```
crewai/
├── main.py              # Main application entry point
├── trip_agents.py       # Agent role definitions
├── trip_tasks.py        # Task implementations
├── tools/               # Utility tools
│   ├── browser_tools.py
│   ├── calculator_tools.py
│   └── search_tools.py
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## 🔧 Implementation Details

### Agent Capabilities

1. **City Selection Expert**
   - Analyzes travel data
   - Considers weather patterns
   - Evaluates seasonal events
   - Compares travel costs

2. **Local Expert**
   - Provides cultural insights
   - Recommends hidden gems
   - Shares local customs
   - Suggests authentic experiences

3. **Travel Concierge**
   - Creates detailed itineraries
   - Manages budget planning
   - Provides packing lists
   - Arranges logistics

### Task Flow

1. **City Selection Phase**
   ```python
   identify_task = tasks.identify_task(
     city_selector_agent,
     origin,
     cities,
     interests,
     date_range
   )
   ```

2. **Local Information Phase**
   ```python
   gather_task = tasks.gather_task(
     local_expert_agent,
     origin,
     interests,
     date_range
   )
   ```

3. **Itinerary Creation Phase**
   ```python
   plan_task = tasks.plan_task(
     travel_concierge_agent, 
     origin,
     interests,
     date_range
   )
   ```

## 🎯 Example Output

The system generates a comprehensive travel plan including:
- Detailed city analysis and selection reasoning
- Local insights and cultural recommendations
- Day-by-day itinerary
- Budget breakdown
- Packing suggestions
- Weather forecasts
- Restaurant and accommodation recommendations

## 🤝 Contributing

We welcome contributions! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📚 Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [Ollama Documentation](https://ollama.ai/docs)
- [Python Documentation](https://docs.python.org/3/)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- CrewAI framework developers
- Ollama team for the LLM support
- Contributors and testers
