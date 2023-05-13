import os

from langchain.llms import OpenAI

from app.components.operations.perform_distilation import PromptDistillation
from app.components.operations.generate_context import ContextGenerator
from app.models.user_intent_model import UserIntent
from app.models.context_model import PromptContext 

#TODO: REMOVE LATER
from langchain import PromptTemplate

from app.components.prompts.prompt_response_generator import PROMPT_RESPONSE_GENERATOR

class ServiceA:
    def __init__(self, state):
        self.llm = OpenAI(
            temperature=0,
            model_name='text-davinci-003',
            openai_api_key=os.environ.get("OPENAI_API_KEY")
        )
        self.prompt_distillation = PromptDistillation()
        self.generate_context = ContextGenerator() 
        self.first_response = True
        self.distillation_phase = state['modifiers']['distillation']

    def perform_operation(self, input_data):
        if input_data == "done" or not self.distillation_phase:
            self.distillation_phase = False
            distillated_prompt = self.prompt_distillation.retrun_distilated_prompt()
            user_model = UserIntent(
                distillated_prompt.get('chat_history'), 
                distillated_prompt.get('summary'), 
                distillated_prompt.get('initial_intention')
                )
            
            context = self.generate_context.perform_context_generation(llm=self.llm, chat_history=user_model.chat_history)
            context_model = PromptContext(
                context.get('creativity_level'),
                context.get('role')
            )
        
            response_type = context_model.response_type
            print(response_type)

            if self.first_response == True: 
                self.first_response = False
                prompt = PromptTemplate(
                    input_variables=["prompt"],
                    partial_variables={
                        "role": context_model.role, 
                        "response_based_on_creativity_level": context_model.response_type,
                        "initial_intention": user_model.initial_intention,
                        "summary": " ".join(user_model.chat_history)},
                    template=PROMPT_RESPONSE_GENERATOR
                    )
                
                promptValue = prompt.format(prompt="Given the initial intention and summary, write your response")
            else:
                prompt = PromptTemplate(
                    input_variables=["prompt"],
                    partial_variables={
                        "role": context_model.role, 
                        "response_based_on_creativity_level": context_model.response_type,
                        "initial_intention": user_model.initial_intention,
                        "summary": user_model.summary},
                    template=PROMPT_RESPONSE_GENERATOR
                    )
                
                promptValue = prompt.format(prompt=user_model.chat_history[-1])

            llm_output = self.llm(promptValue)
            print(llm_output)


        # if self.first_response == True: 
        #         ###
        #         prompt = PromptTemplate(
        #             input_variables=["prompt"],
        #             partial_variables={
        #                 "role": context_model.role, 
        #                 "response_based_on_creativity_level": context_model.response_type,
        #                 "initial_intention": user_model.initial_intention,
        #                 "summary": user_model.summary},
        #             template=PROMPT_RESPONSE_GENERATOR
        #             )
                
        #         promptValue = prompt.format(prompt=user_model.chat_history)
            
        #     llm_output = self.llm(promptValue)
        #     print(llm_output)

        else:
            distillated_prompt = self.prompt_distillation.perform_distillation(llm=self.llm, input_data=input_data)
            print(distillated_prompt)
