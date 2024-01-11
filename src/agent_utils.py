import json
from src.custom_functions import (
    functions_available,
    add_todos,
    complete_todos,
    get_todos,
)
from src.constants import openai_api_key
from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools.convert_to_openai import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.tools import DuckDuckGoSearchRun
from langchain.prompts import MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import AgentExecutor

MEMORY_KEY = "chat_history"

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)
search = DuckDuckGoSearchRun()

chat_history = []


@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, but bad at calculating lengths of words.",
        ),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


tools = [get_word_length, search, get_todos, complete_todos, add_todos]
llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# input1 = "What is the latest movie playing in Bangalore theaters?"
# result = agent_executor.invoke({"input": input1, "chat_history": chat_history})
# chat_history.extend(
#     [
#         HumanMessage(content=input1),
#         AIMessage(content=result["output"]),
#     ]
# )
# for c in chat_history:
#     print(c)
#     print(type(c))
#     print(c.type)

# print(chat_history)
# print(result["output"])
# agent_executor.invoke(
#     {"input": "Add a new todo to watch this on 16th Jan", "chat_history": chat_history}
# )


def get_agent_response(prompt, chat_history):
    print(prompt, chat_history)
    result = agent_executor.invoke({"input": prompt, "chat_history": chat_history})
    print(result)
    return result["output"]
