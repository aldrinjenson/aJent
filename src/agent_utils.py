import streamlit as st
import json
from src.custom_functions import (
    functions_available,
    add_todos,
    complete_todos,
    get_todos,
)
from src.constants import openai_api_key, MEMORY_KEY
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
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from tempfile import TemporaryDirectory
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain.tools import ShellTool


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)
search = DuckDuckGoSearchRun()
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
shell_tool = ShellTool()

shell_tool.description = shell_tool.description + f"args {shell_tool.args}".replace(
    "{", "{{"
).replace("}", "}}")

tools = [wikipedia, search, shell_tool, get_todos, complete_todos, add_todos]
llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

chat_history = []
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, who uses tools when in doubt to help the user. You can open files and play movies using linux tools.",
        ),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


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
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, return_intermediate_steps=True
)


def get_agent_response(prompt, chat_history):
    print(prompt, chat_history)
    thought_process_placeholder = st.empty()
    thought_expander = st.expander("Thought process")

    def slog(msg):
        thought_expander.markdown(msg + "▌")

    for chunk in agent_executor.stream({"input": prompt, "chat_history": chat_history}):
        print(chunk)
        if "actions" in chunk:
            for action in chunk["actions"]:
                slog(
                    f"##### Calling Tool ```{action.tool}``` Input:\n```{action.tool_input}```"
                )
        elif "steps" in chunk:
            for step in chunk["steps"]:
                slog(f"##### Got result: \n```{step.observation}```")
        elif "output" in chunk:
            slog(f"\nOutput received")
            print(chunk)
            print()
            return chunk["output"]
        else:
            raise ValueError
