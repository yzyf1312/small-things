# limit = int(input("Please enter a number for limit:"))
limit = 1000000

num = 2
while(num<=limit):
    isPrime = 1
    if num > 10 and (num % 2 == 0 or num % 10 == 5):
        isPrime = 0
    else:
        i = 2
        while(i*i<=num):
            temp = num % i
            if temp == 0:
                isPrime = 0
            i += 1
    if isPrime:
        print(num)
    num += 1
