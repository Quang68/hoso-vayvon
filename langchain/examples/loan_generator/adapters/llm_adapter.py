from services.llm_service import run_llm

def enrich_data(system_prompt, prompt, user_data):
    return run_llm(system_prompt, prompt, user_data)