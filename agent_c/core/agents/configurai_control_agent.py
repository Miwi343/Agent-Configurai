from agent_c.utils.autogen_config import getautogenconfig

import autogen  # type: ignore
from agent_c.core.skills.get_os import get_os
# from agent_c.core.skills.get_user_input import get_user_input
from agent_c.core.skills.open_shell import open_shell
from agent_c.core.skills.run_command import run_command
from agent_c.core.skills.type_in_shell import type_in_shell
# from agent_c.core.skills.capture_output import capture_output
from agent_c.core.prompts import LLM_PROMPTS

class ControlAgent:
    def __init__(self, name="controlagent"): # type: ignore
        self.name = name
        self.system_message = LLM_PROMPTS["CONTROL_AGENT_PROMPT"]
        self.config_list = getautogenconfig() # type: ignore
        self.number_of_rounds = 10

        print("Creating Configurai Control Agent")
        self.controlagent = autogen.AssistantAgent( # type: ignore
            name=self.name,
            system_message=self.system_message,
            llm_config=self.config_list, # type: ignore
        )
        self.shell_executor = autogen.UserProxyAgent( # type: ignore
            name="shell_proxy",
            is_termination_msg=lambda x: x.get("content", "") and "TERMINATE" in x.get("content", "").rstrip(), # type: ignore
            human_input_mode="NEVER",
            max_consecutive_auto_reply=self.number_of_rounds,
            code_execution_config={
                "work_dir": "coding",
                "use_docker": False,
            }, 
        )
        self.register_skills()

    def register_skills(self):
        self.controlagent.register_for_llm(description=LLM_PROMPTS["GET_OS_PROMPT"])(get_os) # type: ignore
        self.shell_executor.register_for_execution()(get_os) # type: ignore

        # self.controlagent.register_for_llm(description=LLM_PROMPTS["GET_USER_INPUT_PROMPT"])(get_user_input) # type: ignore
        # self.shell_executor.register_for_execution()(get_user_input) # type: ignore

        self.controlagent.register_for_llm(description=LLM_PROMPTS["OPEN_SHELL_PROMPT"])(open_shell) # type: ignore
        self.shell_executor.register_for_execution()(open_shell) # type: ignore

        self.controlagent.register_for_llm(description=LLM_PROMPTS["RUN_COMMAND_PROMPT"])(run_command) # type: ignore
        self.shell_executor.register_for_execution()(run_command) # type: ignore

        #self.controlagent.register_for_llm(description=LLM_PROMPTS["TERMINAL_OUTPUT_PROMPT"])(get_terminal_output) # type: ignore
        #self.shell_executor.register_for_execution()(get_terminal_output) # type: ignore

        self.controlagent.register_for_llm(description=LLM_PROMPTS["TYPE_IN_SHELL_PROMPT"])(type_in_shell) # type: ignore
        self.shell_executor.register_for_execution()(type_in_shell) # type: ignore

        # self.controlagent.register_for_llm(description=LLM_PROMPTS["CAPTURE_OUTPUT_PROMPT"])(capture_output) # type: ignore
        # self.shell_executor.register_for_execution()(capture_output)    # type: ignore
        
