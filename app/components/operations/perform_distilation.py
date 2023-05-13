from langchain import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain import LLMChain

from app.utils.service_a import helpers
from app.components.prompts import prompt_distillation as prompts

# call services from UI - in the future we can call them from API endpoint
# services implement the business logic, uses models and utils

class PromptDistillation:
    def __init__(self):
        self.memory = ConversationBufferMemory(memory_key="prompt_sequence")

    def perform_distillation(self, llm, input_data):
        prompt_template = prompts.PROMP_DISTILLATION
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["prompt_sequence", "user_input"],
        )

        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            verbose=False,
            memory=self.memory
        )

        result = llm_chain.predict(user_input=input_data)

        return result
    
    def retrun_distilated_prompt(self):
        response = helpers.extract_conversation_info(self.memory)
        return response