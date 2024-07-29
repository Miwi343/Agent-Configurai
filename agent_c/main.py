from autogen import Cache # type: ignore

# from agent_c.core.agents.configurai_control_agent import ControlAgent
from core.agents.configurai_planner_agent import PlannerAgent


def system_orchestrator(): # type: ignore
    # Ask for user input for a shell navigation command
    query = input("Enter a shell navigation command: ")

    print("Query: ", query)
    
    # Example of creating an instance of PlannerAgent
    planner_agent_instance = PlannerAgent()

    with Cache.disk() as cache: # type: ignore
        result=planner_agent_instance.planner_executor.initiate_chat( # type: ignore
            planner_agent_instance.planneragent, # self.manager # type: ignore
            max_turns=planner_agent_instance.number_of_rounds,
            message=query,
            silent=False,
            cache=None,
        )
        summary = result.summary # type: ignore
        response = { 'type':'answer', 'content': summary } # type: ignore
    return response # type: ignore

if __name__ == "__main__":
    system_orchestrator()
    