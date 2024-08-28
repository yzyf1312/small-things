#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
	char *str;
	int size = 100; // 初始大小
	int delta = 100;
	str = (char *)malloc(size); // 动态分配初始内存

	if (str == NULL)
	{
		printf("内存分配失败\n");
		return -1;
	}

	printf("请输入：");

	for (size_t i = 0; i < size; i++)
	{
		*(str + i) = getchar();
		if (*(str + i) == '\n')
		{
			*(str + i) = '\0'; // 确保字符串以空字符结尾
			break;
		}
		if (i == size - 1)
		{
			size += delta;
			char *temp = (char *)realloc(str, size); /* 动态调整内存 */
			if (temp == NULL)
			{
				printf("内存分配失败\n");
				free(str); /* 释放原来的内存 */
				return -1;
			}
			str = temp; /* 更新指针 */
		}
	}

	printf("存储的字符串：%s\n", str);

	free(str); /* 释放内存 */
	return 0;
}
