limit = 1000000
primes = []
not_prime = [False] * (limit + 1)  # 初始化一个布尔数组，索引为数，值为是否为质数

for i in range(2, limit + 1):
    if not not_prime[i]:  # 如果当前数i没有被标记为合数
        targetNum = i
        for j in range(i * i, limit + 1, i):  # 从i*i开始，因为i*2, i*3等已经被之前的质数筛过
            not_prime[j] = True  # 将i的倍数标记为合数

print(targetNum)