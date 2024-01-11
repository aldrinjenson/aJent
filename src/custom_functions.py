from langchain.agents import tool

todos = []


@tool
def get_todos(params=None) -> list:
    """
    Returns a list of todos.

    Parameters:
    - params (dict): Additional parameters (currently unused).

    Returns:
    - list: List of todos.
    """
    return todos


@tool
def add_todos(params) -> dict:
    """
    Adds new todos to the existing list.

    Parameters:
    - params (dict): Dictionary containing "todos" key with a list of tasks to add.

    Returns:
    - dict: {"success": True, "message": "Todos added successfully."} on success,
            {"success": False, "message": str(e)} on failure.
    """
    print("params = ")
    print(params)
    try:
        new_todos = params["todos"]
        for todo in new_todos:
            todos.append({"task": todo, "completed": False})
        print("new todo added")
        return {"success": True, "message": "Todos added successfully."}
    except Exception as e:
        return {"success": False, "message": str(e)}


@tool
def complete_todos(params) -> dict:
    """
    Marks specified todos as completed.

    Parameters:
    - params (dict): Dictionary containing "indices" key with a list of indices to mark as completed.

    Returns:
    - dict: {"success": True, "message": "Todos marked as completed successfully."} on success,
            {"success": False, "message": f"Invalid index: {index}"} on invalid index,
            {"success": False, "message": str(e)} on other failures.
    """
    try:
        indices = params["indices"]
        for index in indices:
            if 0 <= index < len(todos):
                todos[index]["completed"] = True
            else:
                return {"success": False, "message": f"Invalid index: {index}"}
        return {"success": True, "message": "Todos marked as completed successfully."}
    except Exception as e:
        return {"success": False, "message": str(e)}


functions_available = {
    "add_todos": add_todos,
    "get_todos": get_todos,
    "complete_todos": complete_todos,
}
