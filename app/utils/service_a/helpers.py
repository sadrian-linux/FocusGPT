from langchain.schema import HumanMessage
from langchain.memory import ConversationSummaryMemory
from langchain.llms import OpenAI

def extract_conversation_info(distillated_prompt):
    
    # 1. Select only human messages
    human_messages = [message.content for message in distillated_prompt.chat_memory.messages if isinstance(message, HumanMessage)]

    memory = ConversationSummaryMemory(llm=OpenAI(temperature=0))
    messages = distillated_prompt.chat_memory.messages
    previous_summary = ""
    summary = memory.predict_new_summary(messages, previous_summary)

    initial_intention = next((message.content for message in distillated_prompt.chat_memory.messages if isinstance(message, HumanMessage)), None)

    response = {
        "chat_history": human_messages,
        "summary": summary,
        "initial_intention": initial_intention
    }

    return response
