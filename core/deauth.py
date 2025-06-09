import subprocess
import os

def run_deauth(interface, ap_mac, client_mac, channel):
    script_path = os.path.join("scripts", "deauth.sh")

    if not os.path.exists(script_path):
        return "[!] Deauth script not found."

    try:
        result = subprocess.run(
            ["sudo", "bash", script_path, interface, ap_mac, client_mac, channel],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"[!] Deauth failed:\n{e.stderr}"
