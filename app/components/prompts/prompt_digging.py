PROMPT_DIGGING_SYSTEM_MESSAGE = """
You are an Expert Planner And Genius In All Knowledge Topics. 
Your role is to assist me in learning new topics and planning for goals.
"""

PROMPT_DIGGING_LAYOUT = """
{prompt_generation_block}
Layout an intelligent 10 step actionable, clear, complete and concise plan to {goal}
"""

PROMPT_DIGGING_BREAKDOWN = """
{prompt_generation_block}
Take step {step} of the plan and break it down into an intelligent 10-step actionable, clear, complete and concise plan. 
Explain the concept and each step of the new plan in detail like for a 10-year old.
"""

PROMPT_DIGGING_EXPAND = """
{prompt_generation_block}
Take step {step}. Explain it in detail and give a clear example of what an expert would do and how. 
After writing the example, explain the reasoning of the expert step by step and the factors taken into account.
"""
