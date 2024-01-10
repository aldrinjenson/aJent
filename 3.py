from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import ShellTool
from langchain_experimental.utilities import PythonREPL
from langchain.agents import Tool
from langchain.tools import DuckDuckGoSearchRun
from src.constants import openai_api_key

# How old is the current president of the US?
python_repl = PythonREPL()
search = DuckDuckGoSearchRun()

shell_tool = ShellTool()

# Create the tool to pass to an agent
# repl_tool = Tool(
#     name="python_repl",
#     description="A Python shell. Use this to execute python commands. If you want to see the output of a value, you should print it out with `print(...)`.",
#     func=python_repl.run,
# )

# Initialize language model
llm = ChatOpenAI(
    temperature=0,
    openai_api_key=openai_api_key,
)

# Initialize agent
self_ask_with_search = initialize_agent(
    [
        shell_tool,
        search,
    ],
    llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

self_ask_with_search.run("what is 2 times the age of the current US president?")
