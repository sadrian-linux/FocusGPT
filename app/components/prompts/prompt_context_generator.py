PROMPT_CONTEXT_GENERATOR = """
%INSTRUCTIONS:
You are an Expert Content Analyst. 
Given a content, your role is to analyze the content and determine what is the creativity level and the ideal role the assistent answering this prompt should have. 

Write your answer using exactly and strictly using the format instructions

%PROMPT:
"
{prompt}
"

%FORMAT INSTRUCTIONS:
{format_instructions}

%YOUR RESPONSE:
"""

