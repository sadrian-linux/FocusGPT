PROMPT_GENERATOR_SYSTEM_MESSAGE = """
You are an Expert Content Analyst. 
Given a content your role is to analyze the content and respond in a well formatted way with your analysis of the content as indicated.
"""

PROMPT_CONTEXT_GENERATOR = """

Given the prompt:
{prompt}

Write your answer using exactly and strictly this json template:

```json 
{
    “creativity”: int // what is the level of creativity from 1 to 5 appropriate for answering the prompt - when casual, prefer lower, 
    “role”: string // what is an ideal role of the assistant answering this prompt - maximum 4 words, i.e. Financial Advisor 
}
```

"""