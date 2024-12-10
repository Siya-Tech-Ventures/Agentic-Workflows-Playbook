import os
from typing import Annotated
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.llms import Ollama
from langgraph.graph import StateGraph, END
from langchain_core.pydantic_v1 import BaseModel

# Define the state of the graph
class GraphState(BaseModel):
    """
    Represents the state of our conversation graph.
    
    Attributes:
        messages (list): List of messages in the conversation
    """
    messages: list = []

# Initialize Ollama model
llm = Ollama(model="llama3.2")

def generate_response(state: GraphState) -> GraphState:
    """
    Generate a response based on the current conversation state.
    
    Args:
        state (GraphState): Current state of the conversation
    
    Returns:
        GraphState: Updated state with the new AI response
    """
    # Get the last human message
    last_message = state.messages[-1]
    
    # Generate response from Ollama
    response = llm.invoke(last_message.content)
    
    # Update the state with the new messages
    return {
        "messages": state.messages + [AIMessage(content=response)]
    }

def route_to_end(state: GraphState) -> str:
    """
    Determine if the conversation should end.
    
    Args:
        state (GraphState): Current state of the conversation
    
    Returns:
        str: Next node in the graph or END
    """
    # Simple logic to end after 3 exchanges
    if len(state.messages) >= 6:  # 3 human + 3 AI messages
        return END
    return "generate"

# Build the graph
def create_conversation_graph():
    """
    Create and compile the conversation graph.
    
    Returns:
        Compiled graph ready for execution
    """
    workflow = StateGraph(GraphState)
    
    # Define the nodes
    workflow.add_node("generate", generate_response)
    
    # Define the edges
    workflow.set_entry_point("generate")
    workflow.add_conditional_edges(
        "generate",
        route_to_end,
        {
            END: END,
            "generate": "generate"
        }
    )
    
    # Compile the graph
    return workflow.compile()

def main():
    """
    Main function to run the LangGraph Ollama demo.
    """
    # Create the graph
    app = create_conversation_graph()
    
    # Start the conversation
    initial_state = GraphState(
        messages=[HumanMessage(content="Tell me a short story about a brave adventurer.")]
    )
    
    # Run the conversation
    final_state = app.invoke(initial_state)
    
    # Print the conversation
    print("Conversation Log:")
    for msg in final_state['messages']:
        if isinstance(msg, HumanMessage):
            print(f"Human: {msg.content}")
        elif isinstance(msg, AIMessage):
            print(f"AI: {msg.content}")

if __name__ == "__main__":
    main()
