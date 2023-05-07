import os

from langchain.llms import OpenAI

from app.components.operations.perform_distilation import PromptDistillation
# call services from UI - in the future we can call them from API endpoint
# services implement the business logic, uses models and utils

# class ServiceA:
#     def __init__(self):
#         self.llm = OpenAI(
#             temperature=0,
#             model_name='text-davinci-003',
#             openai_api_key=os.environ.get("OPENAI_API_KEY")
#         )
#         self.memory = ConversationBufferMemory(memory_key="prompt_sequence")

#     def perform_operation(self, input_data):
#         if input_data == "done":
#             return self.memory

#         prompt_template = prompts.PROMP_DISTILLATION
#         prompt = PromptTemplate(
#             template=prompt_template,
#             input_variables=["prompt_sequence", "user_input"],
#         )

#         llm_chain = LLMChain(
#             llm=self.llm,
#             prompt=prompt,
#             verbose=True,
#             memory=self.memory
#         )

#         result = llm_chain.predict(user_input=input_data)

#         return result
    
class ServiceA:
    def __init__(self):
        self.llm = OpenAI(
            temperature=0,
            model_name='text-davinci-003',
            openai_api_key=os.environ.get("OPENAI_API_KEY")
        )
        self.prompt_distillation = PromptDistillation()

    def perform_operation(self, input_data):
        distillated_prompt = self.prompt_distillation.perform_distillation(llm=self.llm, input_data=input_data)
        print(distillated_prompt)