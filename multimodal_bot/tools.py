from langchain.tools import BaseTool
from langchain_community.tools.file_management.read import ReadFileTool
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
import yfinance as yf
from typing import Optional, Type, Any
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
import python_weather
import asyncio
import os
from pydantic import Field

class StockPriceTool(BaseTool):
    name: str = Field(default="stock_price_checker")
    description: str = Field(default="Useful for getting the current stock price of a company. Input should be the stock symbol.")

    def _run(self, symbol: str) -> str:
        try:
            stock = yf.Ticker(symbol)
            current_price = stock.info['regularMarketPrice']
            return f"The current price of {symbol} is ${current_price}"
        except Exception as e:
            return f"Error fetching stock price: {str(e)}"

    def _arun(self, symbol: str):
        raise NotImplementedError("This tool does not support async")

class WeatherTool(BaseTool):
    name: str = Field(default="weather_checker")
    description: str = Field(default="Get current weather information for a city. Input should be the city name.")

    def _run(self, city: str) -> str:
        try:
            # Run the async function using asyncio
            return asyncio.run(self._get_weather(city))
        except Exception as e:
            return f"Error fetching weather: {str(e)}"

    async def _get_weather(self, city: str) -> str:
        # declare the client with metric units (celsius, km/h, etc.)
        client = python_weather.Client(unit=python_weather.METRIC)
        try:
            # fetch weather data for the city
            weather = await client.get(city)
            
            # Access the first forecast which contains current weather
            if weather and weather.forecasts:
                current = weather.forecasts[0]
                return f"Current weather in {city}: {current.description}, Temperature: {current.temperature}°C"
            else:
                return f"Unable to get weather data for {city}"
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            await client.close()

    def _arun(self, city: str):
        raise NotImplementedError("This tool does not support async")

class WebScraperTool(BaseTool):
    name: str = Field(default="web_scraper")
    description: str = Field(default="Scrape text content from a webpage. Input should be the URL.")

    def _run(self, url: str) -> str:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text()
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            return text[:1000] + "..." if len(text) > 1000 else text
        except Exception as e:
            return f"Error scraping webpage: {str(e)}"

    def _arun(self, url: str):
        raise NotImplementedError("This tool does not support async")

class OCRTool(BaseTool):
    name: str = Field(default="image_text_extractor")
    description: str = Field(default="Extract text from images using OCR. Input should be the absolute path to the image file.")

    def _run(self, image_path: str) -> str:
        try:
            # Verify the file exists and is accessible
            if not os.path.isfile(image_path):
                return f"Error: Image file not found at path: {image_path}"
            
            # Open and process the image
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            
            # Return extracted text or a message if no text was found
            return text.strip() if text.strip() else "No text found in the image."
        except Exception as e:
            return f"Error processing image: {str(e)}"

    def _arun(self, image_path: str):
        raise NotImplementedError("This tool does not support async")

class CSVProcessor(BaseTool):
    name: str = Field(default="csv_processor")
    description: str = Field(default="Process CSV files. Input should be a JSON string with 'path' (file path) and 'operation' ('read', 'head', 'describe', 'columns', 'list', or 'query'). For 'query', include 'query' parameter.")

    def _run(self, input_str: str) -> str:
        try:
            params = json.loads(input_str)
            if not os.path.isfile(params['path']):
                return f"Error: File not found at path: {params['path']}"
            
            df = pd.read_csv(params['path'])
            operation = params.get('operation', 'read')
            
            if operation == 'read':
                return df.to_string()
            elif operation == 'head':
                return df.head().to_string()
            elif operation == 'describe':
                return df.describe().to_string()
            elif operation == 'columns':
                return f"Available columns: {', '.join(df.columns.tolist())}"
            elif operation == 'list':
                if 'column' not in params:
                    return "Error: Column parameter required for 'list' operation"
                
                column = params['column'].lower().strip()
                # Clean up column names for comparison
                df.columns = df.columns.str.replace(' ', '_').str.lower()
                
                if column not in df.columns:
                    return f"Column '{column}' not found. Available columns: {', '.join(df.columns)}"
                
                # Get unique values as a list
                values = df[column].unique().tolist()
                return f"Values in column '{column}':\n" + "\n".join([f"- {str(val)}" for val in values if pd.notna(val)])
            
            elif operation == 'query':
                if 'query' not in params:
                    return "Error: Query parameter required for 'query' operation"
                
                # Clean up column names
                df.columns = df.columns.str.replace(' ', '_').str.lower()
                
                # Get the query and convert to lowercase
                query = params['query'].lower().strip()
                
                try:
                    # If it's just a column name, show unique values
                    if query in df.columns:
                        values = df[query].unique().tolist()
                        return f"Values in column '{query}':\n" + "\n".join([f"- {str(val)}" for val in values if pd.notna(val)])
                    
                    # Parse the query
                    if '==' in query or '>' in query or '<' in query or '>=' in query or '<=' in query:
                        # Split into column and condition
                        parts = None
                        for op in ['>=', '<=', '==', '>', '<']:
                            if op in query:
                                parts = query.split(op)
                                operator = op
                                break
                        
                        if parts and len(parts) == 2:
                            col = parts[0].strip()
                            val = parts[1].strip()
                            
                            # Handle string values
                            if val.startswith("'") and val.endswith("'"):
                                val = val[1:-1]  # Remove quotes
                            elif val.startswith('"') and val.endswith('"'):
                                val = val[1:-1]  # Remove quotes
                            else:
                                # Try to convert to numeric
                                try:
                                    val = float(val)
                                except ValueError:
                                    pass
                            
                            if col not in df.columns:
                                return f"Column '{col}' not found. Available columns: {', '.join(df.columns)}"
                            
                            # Apply the filter
                            if operator == '==':
                                result = df[df[col] == val]
                            elif operator == '>':
                                result = df[df[col] > val]
                            elif operator == '<':
                                result = df[df[col] < val]
                            elif operator == '>=':
                                result = df[df[col] >= val]
                            elif operator == '<=':
                                result = df[df[col] <= val]
                            
                            return result.to_string() if not result.empty else "No matching records found"
                    
                    return f"Invalid query format. Examples:\n" \
                           f"1. Column name (e.g., '{df.columns[0]}')\n" \
                           f"2. Comparison (e.g., '{df.columns[0]} > 10' or '{df.columns[0]} == \"value\"')"
                
                except Exception as e:
                    return f"Error processing query: {str(e)}\n\nAvailable columns: {', '.join(df.columns)}"
            else:
                return f"Error: Unknown operation {operation}. Available operations: read, head, describe, columns, list, query"
        except Exception as e:
            return f"Error processing CSV: {str(e)}"

    def _arun(self, input_str: str):
        raise NotImplementedError("This tool does not support async")

class JSONProcessor(BaseTool):
    name: str = Field(default="json_processor")
    description: str = Field(default="Process JSON files. Input should be a JSON string with 'path' (file path) and 'operation' ('read', 'keys', or 'query'). For 'query', include 'query' parameter with dot notation path.")

    def _run(self, input_str: str) -> str:
        try:
            params = json.loads(input_str)
            if not os.path.isfile(params['path']):
                return f"Error: File not found at path: {params['path']}"
            
            with open(params['path'], 'r') as f:
                data = json.load(f)
            
            operation = params.get('operation', 'read')
            
            if operation == 'read':
                return json.dumps(data, indent=2)
            elif operation == 'keys':
                if isinstance(data, dict):
                    return json.dumps(list(data.keys()), indent=2)
                return "Error: Root element is not a dictionary"
            elif operation == 'query':
                if 'query' not in params:
                    return "Error: Query parameter required for 'query' operation"
                # Process dot notation query (e.g., "data.users.0.name")
                result = data
                for key in params['query'].split('.'):
                    if key.isdigit():  # Handle array indices
                        result = result[int(key)]
                    else:
                        result = result[key]
                return json.dumps(result, indent=2)
            else:
                return f"Error: Unknown operation {operation}"
        except Exception as e:
            return f"Error processing JSON: {str(e)}"

    def _arun(self, input_str: str):
        raise NotImplementedError("This tool does not support async")

def get_tools():
    """Initialize and return all available tools."""
    tools = [
        # File operations
        ReadFileTool(),
        
        # Code execution
        PythonREPLTool(),
        
        # Data processing
        CSVProcessor(),
        JSONProcessor(),
        
        # Research and information
        ArxivQueryRun(),
        WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
        DuckDuckGoSearchRun(),
        YahooFinanceNewsTool(),
        
        # Custom tools
        StockPriceTool(),
        WeatherTool(),
        WebScraperTool(),
        OCRTool(),
    ]
    return tools
