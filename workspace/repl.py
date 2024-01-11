from langchain import hub
from langchain.agents import AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import create_openai_functions_agent
from langchain_openai import ChatOpenAI
from src.constants import openai_api_key

# tools = [PythonREPLTool()]

# instructions = """You are an agent designed to write and execute python code to answer questions.
# You have access to a python REPL, which you can use to execute python code.
# If you get an error, debug your code and try again.
# Only use the output of your code to answer the question.
# You might know the answer without running any code, but you should still run the code to get the answer.
# If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
# """
# base_prompt = hub.pull("langchain-ai/openai-functions-template")
# prompt = base_prompt.partial(instructions=instructions)

# agent = create_openai_functions_agent(
#     ChatOpenAI(
#         temperature=0,
# openai_api_key=openai_api_key,
#     ),
#     tools,
#     prompt,
# )

# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# x = agent_executor.invoke({"input": "What is the 10th fibonacci number?"})
# print(x)


from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import ShellTool


llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=openai_api_key,
)
tools = load_tools(
    [
        # PythonREPLTool(),
        ShellTool()
    ],
    llm=llm,
)

agent = initialize_agent(
    tools, llm, agent="chat-zero-shot-react-description", verbose=True
)

agent.run("Ask the human what they want to do")
