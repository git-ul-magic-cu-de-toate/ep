#include <Windows.h>
#include <malloc.h>

int main()
{
	while (1)
	{
		int * p = (int *)malloc(1024*1024);
		Sleep(100);
	}

	return 0;
}