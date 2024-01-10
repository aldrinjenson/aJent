import json
from src.custom_functions import functions_available
from openai import OpenAI
from src.constants import openai_api_key

client = OpenAI(api_key=openai_api_key)


tools_spec = []

with open("src/tools_spec.json", "r") as json_file:
    tools_spec = json.load(json_file)


def execute_function(function_name, args, **kwargs):
    print(function_name, args)
    try:
        function_to_call = functions_available[function_name]
        result = function_to_call(args)
        return result
    except KeyError:
        return f"Function '{function_name}' not found."


def get_llm_response(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools_spec,
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
    function_resp = execute_function(
        function_name, json.loads(tool_call.function.arguments)
    )
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
