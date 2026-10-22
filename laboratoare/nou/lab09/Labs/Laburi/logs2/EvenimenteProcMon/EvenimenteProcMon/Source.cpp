#include <Windows.h>
#include <stdio.h>

#define FILE_DEVICE_PROCMON_LOG     0x00009535
#define IOCTL_EXTERNAL_LOG_DEBUGOUT	(ULONG) CTL_CODE( FILE_DEVICE_PROCMON_LOG ,\
                                                      0x81                    ,\
                                                      METHOD_BUFFERED         ,\
                                                      FILE_WRITE_ACCESS        )



class MyProcMon
{

	int OpenProcMon()
	{
		hDevice = ::CreateFileW(L"\\\\.\\Global\\ProcmonDebugLogger",
			GENERIC_READ | GENERIC_WRITE,
			FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
			NULL,
			OPEN_EXISTING,
			FILE_ATTRIBUTE_NORMAL,
			NULL);

		if (hDevice == INVALID_HANDLE_VALUE)
		{
			printf("Error opening proc mon log.\n");
			return -1;
		}


		return 0;
	}

	int CloseProcMon()
	{
		CloseHandle(hDevice);
		return 0;
	}

public:
	static HANDLE hDevice;

	static int ProcMonLog(const wchar_t* string)
	{
		//	When runtime flags are OFF open file on constructor
		if (hDevice != INVALID_HANDLE_VALUE)
		{
			DWORD dwLen;
			DWORD dwOut;

			dwLen = (DWORD)wcslen(string) * sizeof(WCHAR);
			::DeviceIoControl(hDevice,
				IOCTL_EXTERNAL_LOG_DEBUGOUT,
				(LPVOID)string,
				dwLen,
				NULL,
				0,
				&dwOut,
				NULL);
		}
		return 0;
	}



	MyProcMon()
	{
		OpenProcMon();
	}


	~MyProcMon()
	{
		CloseProcMon();
	}
};

class ProcMonLogFunc
{
	wchar_t buffer[256];
	const wchar_t * endTrace;
public:
	ProcMonLogFunc(const wchar_t * name)
	{
		_snwprintf_s(buffer, 256, L"==>%s", name);
		MyProcMon::ProcMonLog(buffer);
		endTrace = name;
	}

	~ProcMonLogFunc()
	{
		_snwprintf_s(buffer, 256, L"<==%s", endTrace);
		MyProcMon::ProcMonLog(buffer);
	}

};

#define DBGTRACE_FN_() ProcMonLogFunc __my_log__(__FUNCTIONW__)

HANDLE MyProcMon::hDevice = INVALID_HANDLE_VALUE;
MyProcMon __procMon;



int Func1(HANDLE h)
{
	DBGTRACE_FN_();
	DWORD dwWritten = 0;
	WriteFile(h, "Func1", 5, &dwWritten, NULL);
	return 0;
}

int Func2(HANDLE h)
{
	DBGTRACE_FN_();
	DWORD dwWritten = 0;
	WriteFile(h, "Func2", 5, &dwWritten, NULL);
	return 0;
}

int Func3(HANDLE h)
{
	DBGTRACE_FN_();
	DWORD dwWritten = 0;
	WriteFile(h, "Func3", 5, &dwWritten, NULL);
	return 0;
}


int main()
{
	DBGTRACE_FN_();
	printf("%s\n", __FUNCTION__);

	HANDLE h = CreateFile(L"d:\\out_.txt", GENERIC_READ, FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE, NULL, OPEN_EXISTING, 0, NULL);
	MyProcMon::ProcMonLog(L"Acesta e logul meu 1");
	Func1(h);
	Func2(h);
	Func3(h);
	CloseHandle(h);
	MyProcMon::ProcMonLog(L"Acesta e logul meu 2");

	return 0;
}