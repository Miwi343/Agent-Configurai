from datetime import datetime

import autogen  # type: ignore


from agent_c.core.skills.get_os import get_os
from agent_c.core.skills.open_shell import open_shell
from agent_c.core.skills.run_command import run_command
from agent_c.core.skills.type_in_shell import type_in_shell
from agent_c.core.skills.get_user_input import get_user_input 

from agent_c.core.prompts import LLM_PROMPTS


class ConfiguraiControlAgent:
    def __init__(self, config_list, shell_nav_executor: autogen.UserProxyAgent): # type: ignore
        """
        Initialize the ControlAgent and store the AssistantAgent instance
        as an instance attribute for external access.

        Parameters:
        - config_list: A list of configuration parameters required for AssistantAgent.
        - user_proxy_agent: An instance of the UserProxyAgent class.
        """
        self.shell_nav_executor = shell_nav_executor 
        system_message = LLM_PROMPTS["CONFIGURAI_CONTROL_AGENT_PROMPT"]
        system_message = system_message + "\n" + f"Today's date is {datetime.now().strftime('%d %B %Y')}"


        self.agent = autogen.ConversableAgent(
            name="configurai_control_agent",
            system_message=system_message,
            llm_config={
                "config_list": config_list,
                "cache_seed": 2,
                "temperature": 0.0
            },
        )

        self.__register_skills()

    def __register_skills(self):
        # Register get_os skill for LLM by assistant agent
        self.agent.register_for_llm(description=LLM_PROMPTS["GET_OS_PROMPT"])(get_os)
        # Register get_os skill for execution by user_proxy_agent
        self.shell_nav_executor.register_for_execution()(get_os)

        # Register open_shell skill for LLM by assistant agent
        self.agent.register_for_llm(description=LLM_PROMPTS["OPEN_SHELL_PROMPT"])(open_shell)
        # Register open_shell skill for execution by user_proxy_agent
        self.shell_nav_executor.register_for_execution()(open_shell)

        # Register run_command skill for LLM by assistant agent
        self.agent.register_for_llm(description=LLM_PROMPTS["RUN_COMMAND_PROMPT"])(run_command)
        # Register run_command skill for execution by user_proxy_agent
        self.shell_nav_executor.register_for_execution()(run_command)

        # Register type_in_shell skill for LLM by assistant agent
        self.agent.register_for_llm(description=LLM_PROMPTS["TYPE_IN_SHELL_PROMPT"])(type_in_shell)
        # Register type_in_shell skill for execution by user_proxy_agent
        self.shell_nav_executor.register_for_execution()(type_in_shell)

        # Register get_user_input skill for LLM by assistant agent
        self.agent.register_for_llm(description=LLM_PROMPTS["GET_USER_INPUT_PROMPT"])(get_user_input)
        # Register get_user_input skill for execution by user_proxy_agent
        self.shell_nav_executor.register_for_execution()(get_user_input)

        # print(f">>> Function map: {self.shell_nav_executor.function_map}") # type: ignore
