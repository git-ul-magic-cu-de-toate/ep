#include <Windows.h>
#include <stdio.h>

int main()
{
	char buffer[128];
	HANDLE h = CreateFile(L"good.log", GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE, NULL,
		CREATE_ALWAYS, 0, NULL);
	for (int i = 0; i < 100000; i++)
	{
		_snprintf_s(buffer, 128, "linia numarul %d din log.\n", i + 1);
		DWORD length = strlen(buffer);
		DWORD dwWritten = 0;
		WriteFile(h, buffer, length, &dwWritten, NULL);
	}
	CloseHandle(h);
	return 0;
}