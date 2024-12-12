# Advanced Multimodal Chatbot

A powerful chatbot that combines image processing, natural language understanding, and multiple specialized tools to provide comprehensive responses.

## Features

- 🖼️ **Image Processing**
  - Image description and analysis
  - OCR (Optical Character Recognition)
  - Context-aware image understanding

- 🔍 **Information Retrieval**
  - Web search via DuckDuckGo
  - Wikipedia queries
  - Academic paper search via ArXiv
  - Web scraping capabilities

- 📊 **Data & Analysis**
  - Real-time stock price checking
  - Weather information
  - Financial news updates
  - Python code execution

- 💾 **File Operations**
  - Read and write files
  - List directory contents
  - Process uploaded images

## Installation

### Option 1: Using Conda (Recommended)

1. Install Miniconda or Anaconda if you haven't already:
   - Download from [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/download)
   - Follow the installation instructions for your operating system

2. Create and activate the conda environment:
```bash
# Create environment from yml file
conda env create -f environment.yml

# Activate the environment
conda activate multimodal-bot

# Verify installation
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"
python -c "import transformers; print(f'Transformers version: {transformers.__version__}')"
```

3. Install additional system dependencies (if needed):
   - For OCR functionality (Linux):
     ```bash
     sudo apt-get update && sudo apt-get install -y tesseract-ocr
     ```
   - For macOS:
     ```bash
     brew install tesseract
     ```

### Option 2: Using pip and venv

1. Create a virtual environment (alternative to conda):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

### Environment Setup

1. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your API keys:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add:
     - OpenAI API key (required)
     - Other API keys (optional)

## Usage

1. Activate your environment (if not already activated):
```bash
# If using conda:
conda activate multimodal-bot

# If using venv:
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

4. Try these example queries:
   - "What's the weather in New York?"
   - "What's the stock price of AAPL?"
   - "Search for recent AI papers about transformers"
   - "Upload an image and ask about its contents"
   - "Write a Python function to calculate fibonacci numbers"
   - "What's the latest news about Tesla?"

## Available Tools

The chatbot integrates multiple specialized tools:

- **Search Tools**
  - DuckDuckGo web search
  - Wikipedia queries
  - ArXiv paper search
  - Web scraping

- **Finance Tools**
  - Stock price checker
  - Yahoo Finance news

- **Utility Tools**
  - Weather information
  - OCR text extraction
  - File operations
  - Python REPL

## Technical Details

The chatbot uses:
- LangChain for tool integration and agent orchestration
- Transformers for image analysis
- Streamlit for the web interface
- Various APIs for specialized functions

## Requirements

- Python 3.10+
- CUDA-capable GPU (optional, for faster processing)
- OpenAI API key
- System dependencies (tesseract-ocr for OCR functionality)
- See `environment.yml` or `requirements.txt` for full list of dependencies

## Troubleshooting

### Common Issues

1. **GPU Issues**
   - If you don't have a GPU, remove `cudatoolkit` from `environment.yml`
   - For GPU users, ensure CUDA drivers are properly installed

2. **OCR Issues**
   - Verify tesseract is installed: `tesseract --version`
   - Check system PATH includes tesseract

3. **API Key Issues**
   - Ensure `.env` file exists and contains valid API keys
   - Check for any spaces or quotes in the API key values

### Getting Help

If you encounter issues:
1. Check the error message in the terminal
2. Verify all dependencies are correctly installed
3. Ensure your environment is properly activated
4. Check the versions of your installed packages match the requirements
