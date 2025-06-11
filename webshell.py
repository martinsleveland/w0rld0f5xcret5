import subprocess
import os

def list_available_webshells():
    for webshell in webshells:
        print(webshell)

def run_webshell(script_path, selected_webshell):
    script_path = os.path.join("webshells/", selected_webshell)

    if not os.path.exists(script_path):
        return "[!] Webshell not found."

    try:
        result = subprocess.run(
            ["python", script_path, selected_script],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"[!] Webshell failed:\n{e.stderr}"
