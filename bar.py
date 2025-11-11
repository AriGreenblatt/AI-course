# Todo List Manager
# What You'll Learn
# How Copilot uses existing code patterns to generate consistent code
#The importance of establishing conventions early in your codebase
#How data structure choices influence subsequent suggestions
#Context awareness in code generation
#Success Criteria
# Copilot generates functions that work with your existing data structure
# The coding style remains consistent across functions
# Functions handle the todo list appropriately
# Error handling follows similar patterns
todos = []

def add_todo(task: str, priority: str = "medium"):
    """Add a new todo item with task and priority."""
    todo = {
        "id": len(todos) + 1,
        "task": task,
        "priority": priority,
        "completed": False
    }
    todos.append(todo)
    print(f"Added todo: {task}")

def remove_todo(todo_id: int):
    """Remove a todo by its ID."""
    # Let Copilot implement this
    todos[:] = [todo for todo in todos if todo["id"] != todo_id]
    print(f"Removed todo with ID: {todo_id}")

def mark_completed(todo_id: int):
    """Mark a todo as completed by its ID."""
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = True
            print(f"Marked todo as completed: {todo['task']}")
            break
    else:
        print(f"Todo with ID {todo_id} not found.")


def list_todos(filter_by: str = "all"):
    """List todos. Filter can be 'all', 'completed', or 'pending'."""
    filtered_todos = todos
    if filter_by == "completed":
        filtered_todos = [todo for todo in todos if todo["completed"]]
    elif filter_by == "pending":
        filtered_todos = [todo for todo in todos if not todo["completed"]]

    for todo in filtered_todos:
        status = "✓" if todo["completed"] else "✗"
        print(f"[{status}] {todo['task']} (ID: {todo['id']}, Priority: {todo['priority']})")


def get_todos_by_priority(priority: str):
    """Get all todos with specified priority."""
    return [todo for todo in todos if todo["priority"] == priority]


# Example usage
if __name__ == "__main__":
    print("=== Todo List Manager Demo ===\n")
    
    # Add some todos
    add_todo("Buy groceries", "high")
    add_todo("Write report", "medium")
    add_todo("Call dentist", "low")
    add_todo("Exercise", "medium")
    
    print("\n--- All Todos ---")
    list_todos()
    
    # Mark one as completed
    print("\n--- Marking task as completed ---")
    mark_completed(2)
    
    print("\n--- Updated Todo List ---")
    list_todos()
    
    # Show only pending todos
    print("\n--- Pending Todos Only ---")
    list_todos("pending")
    
    # Show todos by priority
    print("\n--- High Priority Todos ---")
    high_priority = get_todos_by_priority("high")
    for todo in high_priority:
        status = "✓" if todo["completed"] else "✗"
        print(f"[{status}] {todo['task']} (ID: {todo['id']})")
    
    # Remove a todo
    print("\n--- Removing a todo ---")
    remove_todo(3)
    
    print("\n--- Final Todo List ---")
    list_todos()