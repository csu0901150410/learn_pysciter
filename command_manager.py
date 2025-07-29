import json

COMMANDS = {}

def register_command(name):
    def decorator(func):
        COMMANDS[name] = func
        return func
    return decorator

def execute_command(name, json_params = None):
    if name not in COMMANDS:
        return {"error": f"Command '{name}' not registered"}
    
    try:
        if isinstance(json_params, str):
            params = json.loads(json_params) if json_params else {}
        elif isinstance(json_params, dict):
            params = json_params
        else:
            params = {}
        return COMMANDS[name](params)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON parameters: {str(e)}"}
    except Exception as e:
        msg = {"error": str(e)}
        return {"error": str(e)}
