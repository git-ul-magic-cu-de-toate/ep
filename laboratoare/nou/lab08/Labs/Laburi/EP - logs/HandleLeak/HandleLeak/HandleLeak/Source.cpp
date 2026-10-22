#include <Windows.h>


int main()
{
	while (1)
	{
		HANDLE h = CreateFile(L"leak.txt", GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE, NULL, OPEN_ALWAYS, 0, NULL);
		Sleep(100);
	}
	return 0;
}