limit = 1000000000
primes = [True for i in range(limit+1)]

p = 2
while (p * p <= limit):
    if (primes[p] == True):
        for i in range(p * p, limit+1, p):
            primes[i] = False
    p += 1

p = 2
while(p <= limit):
    if primes[p]:
        targetNum = p
    p += 1

print(targetNum)