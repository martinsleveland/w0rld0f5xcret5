import os
import importlib.util

TEMPLATES_DIR = os.path.join("core", "obfuscation_templates")

def list_obfuscation_methods() -> list:
    """
    Returns a list of available obfuscation method names based on python files in the templates directory.
    """
    return [
        f.replace(".py", "")
        for f in os.listdir(TEMPLATES_DIR)
        if f.endswith(".py") and not f.startswith("__")
    ]

def load_obfuscation_function(method_name: str):
    """
    Dynamically imports the obfuscation method module and returns the obfuscate function.
    """
    file_path = os.path.join(TEMPLATES_DIR, f"{method_name}.py")
    
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Obfuscation method '{method_name}' not found.")

    spec = importlib.util.spec_from_file_location(method_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, "obfuscate"):
        return module.obfuscate
    else:
        raise AttributeError(f"Module '{method_name}' does not define an 'obfuscate' function.")

def run_obfuscation(method: str, input_path: str, output_path: str, **kwargs) -> str: # **kwargs means keyword arguments
    """
    Runs the selected obfuscation method.
    """
    if not os.path.isfile(input_path):
        return f"[!] Error: Input file not found → {input_path}"

    try:
        obfuscate_func = load_obfuscation_function(method)
        return obfuscate_func(input_path=input_path, output_path=output_path, **kwargs)
    except Exception as e:
        return f"[!] Error running obfuscation '{method}': {e}"
