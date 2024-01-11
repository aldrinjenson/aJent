todos = []


def get_todos(params=None):
    return todos


def add_todos(params):
    try:
        new_todos = params["todos"]
        for todo in new_todos:
            todos.append({"task": todo, "completed": False})
        return {"success": True, "message": "Todos added successfully."}
    except Exception as e:
        return {"success": False, "message": str(e)}


def complete_todos(params):
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
