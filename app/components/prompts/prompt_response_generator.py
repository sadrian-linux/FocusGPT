PROMPT_RESPONSE_GENERATOR = """
%INSTRUCTIONS:

You are an “Expert {role}”. Answer all future prompts in a manner that is {response_based_on_creativity_level}. 
Use bullet points where applicable and organize the response to be easy to read.

%PROMPT:
“{prompt}”

"""