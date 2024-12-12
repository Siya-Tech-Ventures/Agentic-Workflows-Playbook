import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from tools import get_tools
import tempfile
import json
import datetime
import time
from openai import OpenAI
import os

# Load environment variables
load_dotenv()

class MultiModalBot:
    def __init__(self):
        """Initialize the bot with necessary components."""
        # Initialize OpenAI client
        self.client = OpenAI()
        
        # Initialize chat model
        self.llm = ChatOpenAI(temperature=0.7)
        
        # Initialize memory
        self.memory = []
        
        # Initialize agent with all tools
        self.agent = initialize_agent(
            get_tools(),
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            ),
            verbose=True
        )
        
        # Track current files
        self.current_files = {
            'image': None,
            'csv': None,
            'json': None
        }
    
    def set_file_paths(self, file_type, path):
        """Set the path for a specific file type"""
        self.current_files[file_type] = path
    
    def process_image(self, image, prompt="Describe this image:"):
        # Save image temporarily for OCR if needed
        temp_image_path = None
        try:
            # Create a temporary file with a .png extension
            temp_dir = tempfile.gettempdir()
            temp_image_path = os.path.join(temp_dir, f'temp_image_{os.getpid()}.png')
            
            # Save the image directly to the temporary path
            image.save(temp_image_path, format='PNG')
            self.current_files['image'] = temp_image_path
            
            # Get basic image description
            inputs = self.processor(images=image, text=prompt, return_tensors="pt")
            generated_ids = self.model.generate(
                pixel_values=inputs["pixel_values"],
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_length=50,
            )
            image_description = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            # Try to extract text from image using OCR tool directly
            ocr_tool = [tool for tool in self.agent.tools if tool.name == "image_text_extractor"][0]
            text_content = ocr_tool._run(temp_image_path)
            
            if text_content and text_content != "No text found in the image.":
                return f"{image_description}\n\nText found in image: {text_content}"
            return image_description
            
        finally:
            if temp_image_path and os.path.exists(temp_image_path):
                os.unlink(temp_image_path)

    def chat(self, message: str, image: Image.Image = None) -> str:
        """Process a chat message and return a response."""
        try:
            # Add message to memory
            self.memory.append({"role": "user", "content": message})

            # Get the tools
            tools = get_tools()

            # If there's an image, process it with OCR
            if image:
                # Save image temporarily
                temp_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', f'temp_image_{int(time.time())}.png')
                image.save(temp_image_path)
                self.set_file_paths('image', temp_image_path)

                # Add image context to memory
                self.memory.append({
                    "role": "system",
                    "content": f"An image has been uploaded and is available at: {temp_image_path}"
                })

                # Extract text from image using OCR
                ocr_tool = next((tool for tool in tools if tool.name == "image_text_extractor"), None)
                if ocr_tool:
                    ocr_result = ocr_tool._run(temp_image_path)
                    if ocr_result and not ocr_result.startswith("Error"):
                        self.memory.append({
                            "role": "system",
                            "content": f"Text extracted from image: {ocr_result}"
                        })

            # Prepare messages for the chat
            messages = [
                {"role": "system", "content": """You are a helpful assistant that can process various types of files and answer questions about them. 
                For images, you can extract and analyze text content. For CSV files, you can perform data analysis and answer queries. 
                For JSON files, you can help navigate and extract information."""}
            ]
            
            # Add file paths context if available
            if self.current_files:
                file_context = "Available files:\n"
                for file_type, path in self.current_files.items():
                    if path:  # Only add if path exists
                        file_context += f"- {file_type}: {path}\n"
                messages.append({"role": "system", "content": file_context})

            # Add memory contents
            messages.extend(self.memory[-10:])  # Keep last 10 messages for context

            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=1500,
                tools=[{
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "input": {
                                    "type": "string",
                                    "description": "The input for the tool"
                                }
                            },
                            "required": ["input"]
                        }
                    }
                } for tool in tools]
            )

            # Process the response
            assistant_message = response.choices[0].message
            if assistant_message.tool_calls:
                # Handle tool calls
                tool_outputs = []
                for tool_call in assistant_message.tool_calls:
                    tool = next((t for t in tools if t.name == tool_call.function.name), None)
                    if tool:
                        # Parse the function arguments
                        args = json.loads(tool_call.function.arguments)
                        tool_outputs.append(tool._run(args.get('input', '')))

                # Combine tool outputs into a response
                final_response = "\n".join(tool_outputs) if tool_outputs else "I couldn't process that request."
            else:
                final_response = assistant_message.content

            # Add response to memory
            self.memory.append({"role": "assistant", "content": final_response})

            return final_response

        except Exception as e:
            return f"I encountered an error: {str(e)}. Please make sure you have set up your OpenAI API key in the .env file."

def save_uploaded_file(uploaded_file, file_type):
    """Save uploaded file to the data directory"""
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{file_type}_{timestamp}_{uploaded_file.name}"
    file_path = os.path.join(data_dir, filename)
    
    # Save the file
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getvalue())
    
    return file_path

def main():
    st.set_page_config(page_title="Advanced Multimodal Chatbot", page_icon="🤖", layout="wide")
    st.title("Advanced Multimodal Chatbot 🤖")
    
    # API Keys Management
    with st.sidebar:
        st.header("🔑 API Keys")
        
        # OpenAI API Key (Required)
        openai_key = st.text_input("OpenAI API Key", 
                                 type="password",
                                 value=os.getenv("OPENAI_API_KEY", ""),
                                 help="Required for chat functionality")
        
        # SERPAPI Key (Required)
        serpapi_key = st.text_input("SERPAPI API Key",
                                  type="password",
                                  value=os.getenv("SERPAPI_API_KEY", ""),
                                  help="Required for enhanced search functionality")
        
        # Set environment variables
        if openai_key:
            os.environ["OPENAI_API_KEY"] = openai_key
        if serpapi_key:
            os.environ["SERPAPI_API_KEY"] = serpapi_key
        
        # Show API key status
        missing_keys = []
        if not openai_key:
            missing_keys.append("OpenAI API Key")
        if not serpapi_key:
            missing_keys.append("SERPAPI API Key")
            
        if missing_keys:
            st.error(f"⚠️ Required API Keys missing: {', '.join(missing_keys)}")
            st.stop()
        else:
            st.success("✅ All required API keys are set!")
        
        st.markdown("---")
    
    # Initialize bot in session state if not already done
    if ('bot' not in st.session_state or 
        openai_key != st.session_state.get('last_openai_key', '') or
        serpapi_key != st.session_state.get('last_serpapi_key', '')):
        try:
            st.session_state.bot = MultiModalBot()
            st.session_state.last_openai_key = openai_key
            st.session_state.last_serpapi_key = serpapi_key
        except Exception as e:
            st.error(f"Error initializing bot: {str(e)}")
            st.stop()
        
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Left sidebar with file uploads
    with st.sidebar:
        st.header("Upload Files")
        
        # Image upload
        uploaded_image = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
        if uploaded_image:
            # Display the image
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
            # Convert to PIL Image
            image = Image.open(uploaded_image)
            # Save and set file path
            image_path = save_uploaded_file(uploaded_image, 'image')
            st.session_state.bot.set_file_paths('image', image_path)
            st.success(f"Image saved as: {os.path.basename(image_path)}")
            st.info("You can now ask questions about the image in the chat!")
        
        # CSV upload
        uploaded_csv = st.file_uploader("Upload a CSV file", type=['csv'])
        if uploaded_csv:
            csv_path = save_uploaded_file(uploaded_csv, 'csv')
            st.session_state.bot.set_file_paths('csv', csv_path)
            st.success(f"CSV file saved as: {os.path.basename(csv_path)}")
            st.info("""
            You can now ask questions about your CSV file in the chat:
            - "Show me the first few rows of the CSV"
            - "What columns are in the CSV?"
            - "Show me records where age > 25"
            - "What's the distribution of values in the age column?"
            """)
        
        # JSON upload
        uploaded_json = st.file_uploader("Upload a JSON file", type=['json'])
        if uploaded_json:
            json_path = save_uploaded_file(uploaded_json, 'json')
            st.session_state.bot.set_file_paths('json', json_path)
            st.success(f"JSON file saved as: {os.path.basename(json_path)}")
            st.info("""
            You can now ask questions about your JSON file in the chat:
            - "Show me the contents of the JSON file"
            - "What are the top-level keys in the JSON?"
            - "Show me the value at data.users.0.name"
            """)
    
    # Right sidebar with features and tools
    right_sidebar = st.sidebar.container()
    with right_sidebar:
        st.markdown("---")  # Separator
        st.header("Features & Tools")
        
        # Features section
        st.subheader("🎯 Features")
        features = """
        - 🖼️ Image Analysis & OCR
        - 📊 CSV Data Analysis
        - 📝 JSON Data Processing
        - 💬 Natural Language Chat
        - 🔄 Multi-turn Conversations
        """
        st.markdown(features)
        
        # Tools section
        st.subheader("🛠️ Available Tools")
        tools = """
        - Image Text Extractor (OCR)
        - Stock Price Checker
        - Weather Information
        - Web Scraper
        - Wikipedia Query
        - Arxiv Research
        - JSON Processor
        - Python REPL
        """
        st.markdown(tools)
        
        # Tips section
        st.subheader("💡 Tips")
        tips = """
        - Upload files using the left sidebar
        - Ask questions about uploaded files
        - Combine multiple tools in one query
        - Use natural language for all requests
        """
        st.markdown(tips)
    
    # Chat interface
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # User input
    if prompt := st.chat_input("Ask me anything about your files or any other question..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        # Process the message
        with st.chat_message("assistant"):
            if uploaded_image:
                try:
                    image = Image.open(uploaded_image)
                    response = st.session_state.bot.chat(prompt, image)
                except Exception as e:
                    response = f"Error processing image: {str(e)}"
            else:
                response = st.session_state.bot.chat(prompt)
            
            st.write(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
