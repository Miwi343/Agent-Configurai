import sys
import os
import asyncio
from dotenv import load_dotenv
import openai
from autogen import ConversableAgent, UserProxyAgent, ChatResult # type: ignore

# Ensure the module path is included
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from agent_c.core.agents.configurai_control_agent import ConfiguraiControlAgent
from agent_c.core.agents.high_level_planner_agent import PlannerAgent

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

async def main():
    # Create a UserProxyAgent
    user_proxy_agent = UserProxyAgent(name="user_proxy_agent")

    # Initialize the PlannerAgent with a ConversableAgent
    planner_agent = PlannerAgent(config_list=[], user_proxy_agent=ConversableAgent(name="planner_agent"))

    # Initialize the ConfiguraiControlAgent with a UserProxyAgent
    control_agent = ConfiguraiControlAgent(config_list=[], user_proxy_agent=user_proxy_agent)

    # Get user input from command line
    user_input = input("Please enter your query: ")

    # Start the communication between the planner agent and the control agent
    planner_result= planner_agent.a_initiate_chat( # noqa: F704
        recipient=planner_agent.agent,
        message=user_input,
        clear_history=True,
        silent=False,
        cache=None
    )

    control_result: ChatResult = await control_agent.agent.a_initiate_chat( # noqa: F704
        recipient=control_agent.agent,
        message=planner_result.summary,
        clear_history=True,
        silent=False,
        cache=None
    )

    print(f"\nControl Agent response: {control_result.summary}\n")

if __name__ == "__main__":
    asyncio.run(main())
