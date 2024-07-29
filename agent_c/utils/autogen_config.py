import os
from core.config import (AUTOGEN_MODEL_API_KEY, AUTOGEN_MODEL_NAME)
def getautogenconfig(): # type: ignore
    model_info ={}
    model_info["model"]= AUTOGEN_MODEL_NAME
    model_info["api_key"]= AUTOGEN_MODEL_API_KEY

    if os.getenv("AUTOGEN_MODEL_BASE_URL"):
        model_info["base_url"] = os.getenv("AUTOGEN_MODEL_BASE_URL")

    if os.getenv("AUTOGEN_MODEL_API_TYPE"):
        model_info["api_type"] = os.getenv("AUTOGEN_MODEL_API_TYPE")

    if os.getenv("AUTOGEN_MODEL_API_VERSION"):
        model_info["api_version"] = os.getenv("AUTOGEN_MODEL_API_VERSION")
    
    llm_config = {  # type: ignore
    "config_list": [model_info],
    }
    
    print(llm_config) # type: ignore
    return llm_config # type: ignore