PROMPT_RESPONSE_GENERATOR = """
%INSTRUCTIONS:

You are an “Expert {role}”. Answer all future prompts in a manner that is {response_based_on_creativity_level}.
When answearing the prompt, keep in mind the initial intention of the user and the summary of the previous conversation.

%INITIAL INTENTION:
{initial_intention}

%PREVIOUS CONVERSATION:
{summary}

%PROMPT:
“{prompt}”

%YOUR RESPONSE:
"""