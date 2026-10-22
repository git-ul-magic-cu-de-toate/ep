#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>
#include <Psapi.h>
#include <vector>

/*****************************************************************/
/*                          IMPORTANT                            */
/* You can change any part of the skeleton (even the signatures) */
/*****************************************************************/

// The maximum number of processes
#define MAX_NUM_PROCESSES 1024

// Use this to crash to check if malloc failed
static inline void exitWithErrorNoMemory(PVOID assertVal)
{
    if (!assertVal) {
        printf("Not enough memory, exiting...\n");
        ExitProcess(ENOMEM);
    }
}

static DWORD retrieveProcesses(DWORD* processesIdArray, DWORD arraySize)
{
    // TODO Fill processesIdArray with available processes
    // TODO Return the number of entries returned by the function
    DWORD dwBytesReturned;
    EnumProcesses(processesIdArray, arraySize, &dwBytesReturned);
    return dwBytesReturned / sizeof(DWORD);
}

static HANDLE openProcess(DWORD processId)
{
    // TODO Return a HANDLE from a processId
    return OpenProcess(PROCESS_QUERY_INFORMATION |
        PROCESS_VM_READ,
        FALSE, processId);
}

static void closeProcessList(std::vector<HANDLE>& processHandles, DWORD handleArraySize)
{
    // TODO Close all handles in the list
    for (int i = 0; i < processHandles.size(); i++) {
        CloseHandle(processHandles.at(i));
    }
}

static DWORD processesToHandles(std::vector<HANDLE>& handleArray)
{
    // TODO Retrieve all processes using the retrieveProcesses function
    // TODO Open all process ids (that are positive) with the openProcess function
    // Hint: If the returned handle is > 0, the opening succeeded
    // TODO the number of open handles
    DWORD processesIdArray[MAX_NUM_PROCESSES] = {0};
    DWORD sz = retrieveProcesses(processesIdArray, sizeof(processesIdArray));

    for (int i = 0; i < sz; i++) {
        HANDLE hdl = openProcess(processesIdArray[i]);
        if (hdl != NULL) {
            handleArray.push_back(hdl);
        }
    }
    return handleArray.size();
}

static void getMemoryInfoForHandles(std::vector<HANDLE>& processArray, PPROCESS_MEMORY_COUNTERS counters, DWORD processArraySize)
{
    // TODO Retrieve the memory information for each process in the processArray and fill the data into counters
    int sz = processArray.size();
    for (int i = 0; i < sz; i++) {
        HANDLE hdl = processArray.at(i);
        GetProcessMemoryInfo(hdl, &counters[i], sizeof(counters[i]));
    }
}

static PCHAR* getProcessNameForHandles(std::vector<HANDLE>& processArray, DWORD processArraySize)
{
    // TODO Query for the full process name for each process inside processArray and return an array with all names
    // HINT: Use PROCESS_NAME_NATIVE for the flags if needed
    // HINT: paths can have a maximum length of MAX_PATH
    PCHAR* process_names;
    process_names = (PCHAR*)malloc(processArray.size() * sizeof(PCHAR*));
    int sz = processArray.size();
    for (int i = 0; i < sz; i++) {
        LPSTR pt;
        pt = (LPSTR)malloc(MAX_PATH * sizeof(LPSTR));
        HANDLE hdl = processArray.at(i);
        GetProcessImageFileNameA(hdl, pt, MAX_PATH);
        process_names[i] = pt;
    }
    return process_names;
}

static PERFORMANCE_INFORMATION getSystemInfo()
{
    PERFORMACE_INFORMATION perf = {0};
    // TODO retrieve performance information from the system
    GetPerformanceInfo(&perf, sizeof(perf));
    return perf;
}

// Helper: Parses the full path to extract only the executable
static int extractExecutable(PCHAR pathName)
{
    for (int i = strlen(pathName) - 1; i >= 0; --i) {
        if (pathName[i] == '\\') {
            return i + 1;
        }
    }
    return 0;
}

// Prints all data regarding performance
static void printSystemInfo(PERFORMANCE_INFORMATION perfInfo)
{
    printf("CommitTotal, CommitLimit, CommitPeak, PhysicalTotal, PhysicalAvailable, SystemCache, "
        "KernelTotal, KernelPaged, KernelNonpaged, PageSize, HandleCount, ProcessCount, ThreadCount\n");
    printf("%lld, %lld, %lld, %lld, %lld, %lld, %lld, %lld, %lld, %lld, %lu, %lu, %lu\n\n",
        perfInfo.CommitTotal,
        perfInfo.CommitLimit,
        perfInfo.CommitPeak,
        perfInfo.PhysicalTotal,
        perfInfo.PhysicalAvailable,
        perfInfo.SystemCache,
        perfInfo.KernelTotal,
        perfInfo.KernelPaged,
        perfInfo.KernelNonpaged,
        perfInfo.PageSize,
        perfInfo.HandleCount,
        perfInfo.ProcessCount,
        perfInfo.ThreadCount
    );
}

// Prints all data regarding memory for each process and its name
static void printTableInfo(PPROCESS_MEMORY_COUNTERS memoryCounterData, PCHAR* processNames, DWORD counterSize)
{
    printf("ProcessName, PageFaultCount, PeakWorkingSetSize, WorkingSetSize, QuotaPeakPagedPoolUsage, QuotaPagedPoolUsage, "
        "QuotaPeakNonPagedPoolUsage, QuotaNonPagedPoolUsage, PagefileUsage, PeakPagefileUsage\n");

    for (DWORD i = 0; i < counterSize; i++) {
        printf("%s, %lu, %lld, %lld, %lld, %lld, %lld, %lld, %lld, %lld\n",
            processNames[i] + extractExecutable(processNames[i]),
            memoryCounterData[i].PageFaultCount,
            memoryCounterData[i].PeakWorkingSetSize / 1024,
            memoryCounterData[i].WorkingSetSize / 1024,
            memoryCounterData[i].QuotaPeakPagedPoolUsage / 1024,
            memoryCounterData[i].QuotaPagedPoolUsage / 1024,
            memoryCounterData[i].QuotaPeakNonPagedPoolUsage / 1024,
            memoryCounterData[i].QuotaNonPagedPoolUsage / 1024,
            memoryCounterData[i].PagefileUsage / 1024,
            memoryCounterData[i].PeakPagefileUsage / 1024
        );
    }
}

static void cleanupEnvironment(std::vector<HANDLE>& handleArray, PPROCESS_MEMORY_COUNTERS memoryCounterData, PCHAR* processNames, DWORD openProcesses)
{
    free(memoryCounterData);
    // TODO do cleanup like frees and handle closes here
    // Hint: Free the Handle array
    int sz = handleArray.size();
    closeProcessList(handleArray, handleArray.size());
    for (int i = 0; i < sz; i++) {
        free(processNames[i]);
    }
    free(processNames);
}

int main()
{
    std::vector<HANDLE> handleArray;
    DWORD openProcesses;
    PPROCESS_MEMORY_COUNTERS memoryCounterData;
    PERFORMANCE_INFORMATION perfInfo;
    PCHAR* processNames;

    openProcesses = processesToHandles(handleArray);
    memoryCounterData = (PPROCESS_MEMORY_COUNTERS)calloc(openProcesses, sizeof(PROCESS_MEMORY_COUNTERS));
    exitWithErrorNoMemory(memoryCounterData);
    getMemoryInfoForHandles(handleArray, memoryCounterData, openProcesses);

    processNames = getProcessNameForHandles(handleArray, openProcesses);
    perfInfo = getSystemInfo();
    printSystemInfo(perfInfo);
    printTableInfo(memoryCounterData, processNames, openProcesses);

    cleanupEnvironment(handleArray, memoryCounterData, processNames, openProcesses);
    return 0;
}
