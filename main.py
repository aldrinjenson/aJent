from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL
from langchain.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()
x = search.run("Obama's first name?")
print(x)

# python_repl = PythonREPL()

# x = python_repl.run("print(1+1)")

# print(x)


# # You can create the tool to pass to an agent
# repl_tool = Tool(
#     name="python_repl",
#     description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
#     func=python_repl.run,
# )

# print(repl_tool)
