from openai import OpenAI
import json
from src.constants import openai_api_key

client = OpenAI(
    api_key=openai_api_key,
)
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant that helps the user. Whenever possible try to give the answer without asking for further confirmation from the user.",
    },
    {
        "role": "user",
        "content": "Add a new todo to buy paper towels tomorrow",
        # "content": "Tell me a joke",
    },
]

todos = []


def get_todos(params=None):
    return todos


def add_todos(params):
    print(params)
    params = json.loads(params)
    msg = params["msg"]
    try:
        todos.append({"task": msg, "completed": False})
        return {"success": True, "message": "Todo added successfully."}
    except Exception as e:
        return {"success": False, "message": str(e)}


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_todos",
            "description": "Get the list of todos",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_todos",
            "description": "Add a new todo",
            "parameters": {
                "type": "object",
                "properties": {
                    "msg": {
                        "type": "string",
                        "description": "The task description to add",
                    }
                },
                "required": ["msg"],
            },
        },
    },
]


def execute_function(function_name, args, **kwargs):
    print(function_name, args)
    try:
        function_to_call = globals()[function_name]
        result = function_to_call(args)
        return result
    except KeyError:
        return f"Function '{function_name}' not found."


def run_conversation():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    assistant_message = response.choices[0].message
    print(assistant_message)

    tool_calls = assistant_message.tool_calls

    if not tool_calls:
        print("no tool calls!")
        return assistant_message.content

    tool_call = tool_calls[0]

    function_name = tool_call.function.name
    function_resp = execute_function(function_name, tool_call.function.arguments)
    messages.append(assistant_message)

    messages.append(
        {
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": json.dumps(function_resp),
        }
    )
    second_response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
    )
    response_message = second_response.choices[0].message
    messages.append(response_message)

    print(response_message)
    return response_message.content


print(run_conversation())
