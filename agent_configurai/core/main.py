import sys
import os
import asyncio
from dotenv import load_dotenv
import openai

# Ensure the module path is included
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from agent_configurai.core.configurai_control_agent import ConfiguraiControlAgent

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

def main():
    # Initialize the ConfiguraiControlAgent
    agent = ConfiguraiControlAgent(config_list=[], user_proxy_agent=None)
    
    # Run the agent (assuming run_conversation is an asyncio coroutine)
    asyncio.run(agent.run_conversation())

if __name__ == "__main__":
    main()
