void main() {
  int limit = 1000000;
  int num = 2;
  int i;
  bool isPrime;

  while (num <= limit) {
    isPrime = true;
    if (num > 10 && (num % 2 == 0 || num % 10 == 5)) {
      isPrime = false;
    } else {
      i = 2;
      while (i * i <= num) {
        if ((num % i) == 0) {
          isPrime = false;
        }
        i++;
      }
    }
    if (isPrime) {
      print(num);
    }
    num++;
  }
}
