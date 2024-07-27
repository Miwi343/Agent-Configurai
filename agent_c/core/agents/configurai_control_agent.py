from datetime import datetime

import autogen  # type: ignore
from dotenv import load_dotenv
import os
from typing import Optional, List, Dict, Any, Tuple

from agent_c.core.skills import get_os, open_shell, run_command, type_in_shell, get_user_input
from agent_c.core.prompts import LLM_PROMPTS

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ConfiguraiControlAgent:
    def __init__(self, config_list: List[Dict[str, Any]], user_proxy_agent: Optional[autogen.UserProxyAgent] = None) -> None:
        """
        Initialize the ConfiguraiControlAgent with the provided configuration list and user proxy agent.
        :param config_list: List of dictionaries containing configuration settings.
        :param user_proxy_agent: Optional user proxy agent instance. If not provided, a new instance will be created.
        :return: None
        """
        self.user_proxy_agent = user_proxy_agent or self.create_user_proxy_agent()
        system_message = self.__generate_system_message()

        self.agent = autogen.ConversableAgent(
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

    def __generate_system_message(self) -> str:
        system_message = LLM_PROMPTS["CONFIGURAI_CONTROL_AGENT_PROMPT"]
        system_message = system_message + "\n" + f"Today's date is {datetime.now().strftime('%d %B %Y')}"
        return system_message

    def __register_skills(self):
        # Register get_os skill for LLM by assistant agent
        self.agent.register_for_llm(description=LLM_PROMPTS["GET_OS_PROMPT"])(get_os.get_os)
        # Register get_os skill for execution by user_proxy_agent
        self.user_proxy_agent.register_for_execution()(get_os.get_os)

        # Register open_shell skill for LLM by assistant agent
        self.agent.register_for_llm(description=LLM_PROMPTS["OPEN_SHELL_PROMPT"])(open_shell.open_shell)
        # Register open_shell skill for execution by user_proxy_agent
        self.user_proxy_agent.register_for_execution()(open_shell.open_shell)

        # Register run_command skill for LLM by assistant agent
        self.agent.register_for_llm(description=LLM_PROMPTS["RUN_COMMAND_PROMPT"])(run_command.run_command)
        # Register run_command skill for execution by user_proxy_agent
        self.user_proxy_agent.register_for_execution()(run_command.run_command)

        # Register type_in_shell skill for LLM by assistant agent
        self.agent.register_for_llm(description=LLM_PROMPTS["TYPE_IN_SHELL_PROMPT"])(type_in_shell.type_in_shell)
        # Register type_in_shell skill for execution by user_proxy_agent
        self.user_proxy_agent.register_for_execution()(type_in_shell.type_in_shell)

        # Register get_user_input skill for LLM by assistant agent
        self.agent.register_for_llm(description=LLM_PROMPTS["GET_USER_INPUT_PROMPT"])(get_user_input.get_user_input)
        # Register get_user_input skill for execution by user_proxy_agent
        self.user_proxy_agent.register_for_execution()(get_user_input.get_user_input)

        self.agent.register_reply(reply_func=self.print_message_from_agent) # type: ignore

    def print_message_from_agent(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]):
        pass

    def is_termination_message(self, message: Dict[str, Any]) -> bool:
        content = message.get("content", "")
        return isinstance(content, str) and content.rstrip().endswith("##TERMINATE##")

    # async def run_conversation(self):
    #     # Print the OS information at the start
    #     os_info = get_os.get_os()
    #     os_message = (
    #         f"Your current system is running on {os_info['system']} OS. "
    #         f"The node is {os_info['node']}, the release version is {os_info['release']}, "
    #         f"and the machine is {os_info['machine']}. The processor is {os_info['processor']}. "
    #         f"You are running {os_info['system']} version {os_info.get('macos_version', os_info['release'])}."
    #     )
    #     print(f"\n{os_message}\n")

    #     while True:
    #         user_input = input("Enter your command: ")
    #         if user_input.lower() == "exit":
    #             break
            
    #         if "open terminal" in user_input.lower():
    #             await open_shell.open_shell()
    #             print("\nNow, I will open your terminal.\n")
    #         else:
    #             # Execute other commands using autogen
    #             result: Coroutine[Any, Any, autogen.ChatResult] = self.user_proxy_agent.a_initiate_chat(
    #                 recipient=self.agent,
    #                 message=user_input,
    #                 cache=None
    #             )

    #             chat_result: autogen.ChatResult = await result
    #             summary = chat_result.summary
    #             response = {'type': 'answer', 'content': summary}
    #             print(f"\nAgent response: {response}\n")

if __name__ == "__main__":
    agent = ConfiguraiControlAgent(config_list=[], user_proxy_agent=None)
    # asyncio.run(agent.run_conversation())
