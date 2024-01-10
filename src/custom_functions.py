todos = []


def get_todos(params=None):
    return todos


def add_todos(params):
    msg = params["msg"]
    try:
        todos.append({"task": msg, "completed": False})
        return {"success": True, "message": "Todo added successfully."}
    except Exception as e:
        return {"success": False, "message": str(e)}


functions_available = {"add_todos": add_todos, "get_todos": get_todos}
