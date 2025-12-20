def get_system_prompt(context: str = "") -> str:
    """
    Generate the system prompt for the Physical AI Teaching Assistant
    """
    base_prompt = "You are a Physical AI Teaching Assistant. Use the provided context to answer. If unsure, admit it."

    if context:
        return f"{base_prompt}\n\n{context}"
    else:
        return base_prompt