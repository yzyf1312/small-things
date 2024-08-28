void main() {
  int limit = 1000000000;
  List<bool> primes = List.filled(limit + 1, true); // 初始化列表，填充true
  int i, p;
  int? targetNum;

  p = 2;
  while (p * p <= limit) {
    if (primes[p]) {
      i = p * p;
      while (i <= limit) {
        primes[i] = false;
        i += p;
      }
    }
    p++;
  }

  p = 2;
  while (p <= limit) {
    if (primes[p]) {
      targetNum = p;
    }
    p++;
  }
  print(targetNum);
}
