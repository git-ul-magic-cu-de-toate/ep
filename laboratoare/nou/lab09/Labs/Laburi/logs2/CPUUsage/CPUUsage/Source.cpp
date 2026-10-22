#include <Windows.h>

int a = 0;

int CPUFunc()
{
	a++;
	return 0;
}

int main()
{
	for (int i = 0; i < 1000000000; i++)
		CPUFunc();
	return 0;
}