from langchain import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

from app.components.prompts import prompt_context_generator as prompts


class ContextGenerator:
    def __init__(self):
        self.response_schemas = [
            ResponseSchema(name="creativity_level", description="an int that determines the level of creativity from 1 to 5 appropriate for answering the prompt - when casual, prefer lower", type="int"),
            ResponseSchema(name="role", description="what is an ideal role of the assistant answering this prompt - maximum 4 words, i.e. Financial Advisor - should be a string", type="str")
            ]

    def perform_context_generation(self, llm, chat_history):
            
        output_parser = StructuredOutputParser.from_response_schemas(self.response_schemas)
        format_instructions = output_parser.get_format_instructions()

        prompt = PromptTemplate(
            input_variables=["prompt"],
            partial_variables={"format_instructions": format_instructions},
            template=prompts.PROMPT_CONTEXT_GENERATOR)

        promptValue = prompt.format(prompt=chat_history)
        llm_output = llm(promptValue)
        
        result = output_parser.parse(llm_output)
        return result
