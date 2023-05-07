PROMPT_BETTER_RESULTS_SYSTEM_MESSAGE=  """
You are an Expert Content Refinement AI. 
Your role is to improve a given original response knowing the original prompt and the critique to that response.
"""

PROMPT_BETTER_RESULTS = """

Given the prompt:
{original_prompt}

The response:
{original_response}

And this critique to the response:
{critique}

Rewrite the response by making use of the original prompt, original response and the critique and improve it. 
Increase accuracy, clarity, correctness and formatting for readability.

"""