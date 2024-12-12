# Advanced Multimodal Chatbot

A powerful AI chatbot that combines image processing, natural language understanding, and multiple specialized tools to provide comprehensive responses.

![Multimodal Chatbot Interface](thumbnail.webp)

> 🤖 A versatile chatbot that can process images, answer questions, analyze data, and more!

## 🎯 Key Highlights

- 🖼️ Process and analyze images with OCR
- 🔍 Search across multiple sources (Web, Wikipedia, ArXiv)
- 📊 Handle data files (CSV, JSON) with ease
- 🌐 Get real-time information (Weather, Stocks, News)
- 🧮 Perform computations with Wolfram Alpha
- 💬 Natural language interface for all operations

## 🌟 Features

### 🖼️ Image Processing
- Image description and analysis
- OCR (Optical Character Recognition)
- Context-aware image understanding
- Support for PNG, JPG, and JPEG formats

### 🔍 Information Retrieval
- Web search via DuckDuckGo
- Wikipedia queries and summaries
- Academic paper search via ArXiv
- Web scraping capabilities
- Enhanced search with SERPAPI

### 📊 Data & Analysis
- Real-time stock price checking
- Weather information worldwide
- Financial news updates
- Mathematical computations (via Wolfram Alpha)
- Python code execution
- CSV and JSON file processing

### 💾 File Operations
- Read and write files
- List directory contents
- Process uploaded images
- CSV data analysis
- JSON data manipulation

## 🚀 Quick Start

1. **Clone the Repository**
```bash
git clone <repository-url>
cd multimodal_bot
```

2. **Environment Setup**

Choose one of these options:

### Option A: Using Conda (Recommended)
```bash
# Create environment
conda env create -f environment.yml

# Activate environment
conda activate multimodal-bot
```

### Option B: Using pip and venv
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. **API Keys Setup**

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
# Required
OPENAI_API_KEY=your_openai_key_here
SERPAPI_API_KEY=your_serpapi_key_here

# Optional (for enhanced features)
WOLFRAM_ALPHA_API_KEY=your_wolfram_key_here
```

4. **Run the App**
```bash
streamlit run app.py
```

## 💡 Usage Examples

### Image Analysis
- Upload an image and ask questions about it
- Extract text from images using OCR
- Get detailed descriptions of image content

### Data Processing
- "Show me the first 5 rows of my CSV file"
- "What's the average value in column X?"
- "Find all JSON entries where age > 25"

### Information Queries
- "What's the current weather in London?"
- "Get me the latest stock price for AAPL"
- "Search for recent papers about machine learning"
- "Solve this mathematical equation: 2x^2 + 3x = 10"

### Web Interactions
- "Summarize the content from this URL"
- "Find recent news about artificial intelligence"
- "Get me information about quantum computing from Wikipedia"

## 🛠️ Available Tools

- **Image Tools**
  - Image Text Extractor (OCR)
  - Image Description Generator
  
- **Data Tools**
  - Stock Price Checker
  - Weather Information
  - CSV Processor
  - JSON Processor
  
- **Search Tools**
  - Web Scraper
  - Wikipedia Query
  - ArXiv Research
  - SERP API Search
  
- **Computation Tools**
  - Python REPL
  - Wolfram Alpha Calculator

## 🔧 System Requirements

- Python 3.9 or higher
- 4GB RAM minimum (8GB recommended)
- Internet connection for API access
- Disk space: ~500MB for dependencies

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

## ⚠️ Important Notes

- Keep your API keys secure and never commit them to version control
- Some features require specific API keys to function
- The app uses streaming responses, so a stable internet connection is recommended
- Large files (>100MB) may take longer to process
