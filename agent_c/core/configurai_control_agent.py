from string import Template
import autogen  # type: ignore
from dotenv import load_dotenv
import os
import asyncio
from typing import Optional, List, Dict, Any, Tuple, Coroutine

from agent_c.core.skills import get_os, open_shell, run_command, type_in_shell
from agent_c.core.prompts import LLM_PROMPTS

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ConfiguraiControlAgent:
    def __init__(self, config_list: List[Dict[str, Any]], user_proxy_agent: Optional[autogen.UserProxyAgent] = None):
        self.user_proxy_agent = user_proxy_agent or self.create_user_proxy_agent()
        user_ltm = self.__get_ltm()
        system_message = self.__generate_system_message(user_ltm)
        
        self.agent = autogen.AssistantAgent(
            name="configurai_control_agent",
            system_message=system_message,
            llm_config={
                "config_list": [{"model": "gpt-4", "api_key": OPENAI_API_KEY}],
                "cache_seed": 2,
                "temperature": 0.0
            },
        )

        self.__register_skills()

    def create_user_proxy_agent(self) -> autogen.UserProxyAgent:
        return autogen.UserProxyAgent(
            name="user_proxy_agent",
            is_termination_msg=self.is_termination_message,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            code_execution_config={
                "work_dir": "coding",
                "use_docker": False,
            },
        )

    def __get_ltm(self) -> Optional[str]:
        return None

    def __generate_system_message(self, user_ltm: Optional[str]) -> str:
        system_message = LLM_PROMPTS["CONFIGURAI_AGENT_PROMPT"]
        if user_ltm:
            user_ltm = "\n" + user_ltm
        else:
            user_ltm = ""

        os_info = get_os.get_os()
        os_message = (
            f"Your current system is running on {os_info['system']} OS. "
            f"The node is {os_info['node']}, the release version is {os_info['release']}, "
            f"and the machine is {os_info['machine']}. The processor is {os_info['processor']}. "
            f"You are running {os_info['system']} version {os_info.get('macos_version', os_info['release'])}."
        )

        return Template(system_message).substitute(basic_user_information=user_ltm + "\n" + os_message)

    def __register_skills(self):
        self.user_proxy_agent.register_for_execution()(get_os.get_os)
        self.agent.register_for_llm(description="Retrieve the OS information of the user's machine.")(get_os.get_os)

        self.user_proxy_agent.register_for_execution()(open_shell.open_shell)
        self.agent.register_for_llm(description="Open a terminal or command prompt.")(open_shell.open_shell)

        self.user_proxy_agent.register_for_execution()(type_in_shell.type_in_shell)
        self.agent.register_for_llm(description="Type necessary commands into the terminal.")(type_in_shell.type_in_shell)

        self.user_proxy_agent.register_for_execution()(run_command.run_command)
        self.agent.register_for_llm(description="Execute the typed terminal command.")(run_command.run_command)

    def print_message_from_user_proxy(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]):
        pass

    def print_message_from_agent(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]):
        pass

    def is_termination_message(self, message: Dict[str, Any]) -> bool:
        content = message.get("content", "")
        return isinstance(content, str) and content.rstrip().endswith("##TERMINATE##")

    async def run_conversation(self):
        # Print the OS information at the start
        os_info = get_os.get_os()
        os_message = (
            f"Your current system is running on {os_info['system']} OS. "
            f"The node is {os_info['node']}, the release version is {os_info['release']}, "
            f"and the machine is {os_info['machine']}. The processor is {os_info['processor']}. "
            f"You are running {os_info['system']} version {os_info.get('macos_version', os_info['release'])}."
        )
        print(f"\n{os_message}\n")

        while True:
            user_input = input("Enter your command: ")
            if user_input.lower() == "exit":
                break
            
            if "open terminal" in user_input.lower():
                await open_shell.open_shell()
                print("\nNow, I will open your terminal.\n")
            else:
                # Execute other commands using autogen
                result: Coroutine[Any, Any, autogen.ChatResult] = self.user_proxy_agent.a_initiate_chat(  # type: ignore
                    recipient=self.agent,
                    message=user_input,
                    cache=None
                )

                chat_result: autogen.ChatResult = await result
                summary = chat_result.summary
                response = {'type': 'answer', 'content': summary}
                print(f"\nAgent response: {response}\n")

if __name__ == "__main__":
    agent = ConfiguraiControlAgent(config_list=[], user_proxy_agent=None)
    asyncio.run(agent.run_conversation())
