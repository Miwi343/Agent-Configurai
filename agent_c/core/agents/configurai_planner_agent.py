from typing import Any
from agent_c.utils.autogen_config import getautogenconfig
import autogen  # type: ignore
import json 

from agent_c.core.prompts import LLM_PROMPTS
from agent_c.core.agents.configurai_control_agent import ControlAgent

class PlannerAgent:
    def __init__(self, name="planneragent"): # type: ignore
        self.name = name
        self.system_message = LLM_PROMPTS["PLANNER_AGENT_PROMPT"]
        self.config_list = getautogenconfig() # type: ignore
        self.number_of_rounds = 10
        self.hierarchial_execution = True


        print("Creating Configurai Planner Agent")
        self.planneragent = autogen.AssistantAgent( # type: ignore
            name=self.name,
            system_message=self.system_message,
            llm_config=self.config_list, # type: ignore
        )
        self.planner_executor = autogen.UserProxyAgent( # type: ignore
            name="user",
            llm_config=False,
            is_termination_msg=self.is_planner_termination_message, # type: ignore
            human_input_mode="NEVER",
            max_consecutive_auto_reply=self.number_of_rounds,
            code_execution_config={
                "work_dir": "coding",
                "use_docker": False,
            }, 
        )
        if self.hierarchial_execution:
            self.nested_agent=ControlAgent()
            self.planner_executor.register_nested_chats( # type: ignore
            [
                {
                "sender": self.nested_agent.controlagent, # type: ignore
                "recipient": self.nested_agent.shell_executor, # type: ignore
                "message":self.reflection_message, # type: ignore
                "max_turns": self.number_of_rounds,
                "summary_method": self.my_custom_summary_method, # type: ignore
                }
            ],
            trigger=self.trigger_nested_chat, # type: ignore
        )

    def parse_response(self, content: str)->dict[str, Any]: 
        """
        Parse the response from the planner agent into a json.
        """
        # type: ignore
        # ideally, this should be a json response, but often it may not be. 
        # So, we will need to do a string based parsing as a back up.        
        return json.loads(content)
        
    def is_planner_termination_message(self, x: dict[str, str])->bool: # type: ignore
        """
        Check if the message is a termination message for the planner agent. 
        If content is empty or terminate is yes, then it is a termination message.
        """
        should_terminate = False
        function: Any = x.get("function", None)
        if function is not None:
            return False

        content:Any = x.get("content", "")
        if content is None:
            content = ""
            should_terminate = True
        else:
            content_json = self.parse_response(content)
            _terminate = content_json.get('terminate', "no")
            if _terminate == "yes":
                should_terminate = True
        return should_terminate # type: ignore

    def trigger_nested_chat(self,manager: autogen.ConversableAgent): # type: ignore
        """
        Condition for triggering the nested chat.
        Trigger nested chat if the next step is not None.
        """
        content:str=manager.last_message()["content"] # type: ignore
        content_json = self.parse_response(content) # type: ignore
        next_step = content_json.get('next_step', None)
        if next_step is None:
            return False
        else:
            return True

    def my_custom_summary_method(self,sender: autogen.ConversableAgent,recipient: autogen.ConversableAgent, summary_args: dict ) : # type: ignore
        """
        Return a response to the planner from the nested chat.
        it is the last message (without the TEMINATE) from the nested chat.
        """
        last_message=recipient.last_message(sender)["content"] # type: ignore
        if not last_message or last_message.strip() == "": # type: ignore
            return "I received an empty message. Try a different approach."
        elif "TERMINATE" in last_message:
            last_message=last_message.replace("TERMINATE", "") # type: ignore
            return last_message #  type: ignore
        return recipient.last_message(sender)["content"] # type: ignore

    def reflection_message(self, recipient, messages, sender, config): # type: ignore
        """
        Pass the task to the nested chat.
        The string in the next_step is passed to the nested chat.
        """
        last_message=messages[-1]["content"] # type: ignore
        content_json = self.parse_response(last_message) # type: ignore
        next_step = content_json.get('next_step', None)

        if next_step is None:
            print ("Message to nested chat returned None")
            return None
        else:
            return next_step # type: ignore
