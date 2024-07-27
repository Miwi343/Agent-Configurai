from typing import Annotated

def get_user_input() -> Annotated[str, "User input query"]:
    """
    This skill gets user input through the command line.
    """
    user_input = input("Please enter your query: ")
    return user_input

if __name__ == "__main__":
    query = get_user_input()
    print(f"User input: {query}")
