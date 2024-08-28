#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <inttypes.h>
#include <string.h>

#define CRC32_POLY 0xEDB88320

// CRC32计算函数声明
uint32_t crc32_byte(uint32_t crc, uint8_t byte);
uint32_t crc32_bytes(uint32_t crc, const uint8_t *buffer, size_t length);
uint32_t file_crc32(const char *filepath);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s <number_of_bytes>\n", argv[0]);
        return 1;
    }

    // 获取字节数
    size_t file_size = atol(argv[1]);
    FILE *file = fopen("temp.bin", "wb");

    if (!file)
    {
        perror("Error opening file");
        return 1;
    }

    // 初始化随机数生成器
    srand((unsigned int)time(NULL));

    // 生成随机文件
    for (size_t i = 0; i < file_size; ++i)
    {
        unsigned char random_byte = (unsigned char)(rand() % 256);
        fwrite(&random_byte, sizeof(random_byte), 1, file);
    }

    fclose(file);

    // 计算CRC32并重命名文件
    if (file_size > 0) // 确保文件大小不为0
    {
        const char *tempfilepath = "temp.bin";
        uint32_t crc32_value = file_crc32(tempfilepath);
        char crc32Hex[9];
        sprintf(crc32Hex, "%08" PRIX32, crc32_value); // 使用PRIX32宏确保正确格式化为十六进制
        char targetFilename[256];                     // 确保数组足够大以存储文件名和CRC32值
        snprintf(targetFilename, sizeof(targetFilename), "%s_%s.bin", "temp", crc32Hex);
        rename(tempfilepath, targetFilename);
        printf("Random file of size %ld bytes has been created with CRC32: %s\n", file_size, crc32Hex);
    }

    return 0;
}

// 定义crc32_byte函数
uint32_t crc32_byte(uint32_t crc, uint8_t byte)
{
    crc ^= byte;
    for (int j = 8; j != 0; --j)
    {
        crc = (crc >> 1) ^ ((crc & 1) ? CRC32_POLY : 0);
    }
    return crc;
}

// 定义crc32_bytes函数
uint32_t crc32_bytes(uint32_t crc, const uint8_t *buffer, size_t length)
{
    for (size_t i = 0; i < length; i++)
    {
        crc = crc32_byte(crc, buffer[i]);
    }
    return crc;
}

// 读取文件并计算CRC32
uint32_t file_crc32(const char *filepath)
{
    FILE *file = fopen(filepath, "rb");
    if (!file)
    {
        perror("Error opening file");
        exit(EXIT_FAILURE);
    }

    uint32_t crc = 0xffffffff;
    uint8_t buffer[1024];
    size_t bytesRead;

    while ((bytesRead = fread(buffer, 1, sizeof(buffer), file)) > 0)
    {
        crc = crc32_bytes(crc, buffer, bytesRead);
    }

    fclose(file);
    return crc ^ 0xffffffff;
}