#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <windows.h>
#else
#include <time.h>
#endif

// 根据平台获取当前时间的函数
void getTime(double* seconds) {
    #ifdef _WIN32
    LARGE_INTEGER freq, counter;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&counter);
    *seconds = (double)counter.QuadPart / freq.QuadPart;
    #else
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC_RAW, &ts);
    *seconds = ts.tv_sec + ts.tv_nsec / 1e9;
    #endif
}

int main(int argc, char* argv[]) {
    double startTime, endTime, duration;
    char command[1024] = {0};

    // 检查命令行参数
    if (argc > 1) {
        snprintf(command, sizeof(command), "%s", argv[1]);
    } else {
        printf("Please enter the command:");
        fgets(command, sizeof(command), stdin);
        command[strcspn(command, "\n")] = 0; // 去除换行符
    }

    // 获取开始时间
    getTime(&startTime);

    // 执行命令
    system(command);

    // 获取结束时间
    getTime(&endTime);

    // 计算持续时间（毫秒）
    duration = (endTime - startTime) * 1000;
    printf("The command '%s' ran for: %.2f milliseconds.\n", command, duration >= 0 ? duration : -duration);

    return 0;
}
