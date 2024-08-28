#include <stdio.h>
#include <stdlib.h> // for "malloc" and "free"
#include <stdbool.h>

int main(void)
{
    int limit = 1000000000;
    bool *not_prime = (bool *)malloc((limit + 1) * sizeof(bool));
    int targetNum = 0;
    int i, j;

    i = 0;
    while (i <= limit)
    {
        not_prime[i] = false;
        i++;
    }

    i = 2;
    while (i <= limit)
    {
        if (!not_prime[i])
        {
            targetNum = i;
            j = i * i;
            while (j <= limit)
            {
                not_prime[j] = true;
                j += i;
            }
        }
        i++;
    }
    printf("%d", targetNum);

    free(not_prime);
}
