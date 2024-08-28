#include <stdio.h>
#include <stdlib.h> // for "malloc" and "free"
#include <stdbool.h>

int main(void)
{
    int limit = 1000000000;
    int i, p;
    bool *primes = (bool *)malloc((limit + 1) * sizeof(bool));
    int targetNum;

    i = 0;
    while (i <= limit)
    {
        primes[i] = true;
        i++;
    }

    p = 2;
    while (p * p <= limit)
    {
        if (primes[p])
        {
            i = p * p;
            while (i <= limit)
            {
                primes[i] = false;
                i += p;
            }
        }
        p++;
    }

    p = 2;
    while (p <= limit)
    {
        if (primes[p])
        {
            targetNum = p;
        }
        p++;
    }
    printf("%d\n", targetNum);

    free(primes);
}