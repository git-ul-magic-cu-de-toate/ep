#include <vld.h>
#include <Windows.h>
#include <malloc.h>

int main()
{
	int i = 0;
	while (i< 10)
	{
		int * p = (int *)malloc(1024*1024);
		Sleep(100);
		i++;
	}

	return 0;
}