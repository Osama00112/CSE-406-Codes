import random

def power(x, y, p):
	
	# Initialize result
	res = 1;

	x = x % p;
	while (y > 0):		
		if (y & 1):
			res = (res * x) % p;

		# y must be even now
		y = y>>1; # y = y/2
		x = (x * x) % p;
	
	return res;

def millerTest(d, n):
	a = 2 + random.randint(1, n - 4);
	# Compute a^d % n
	x = power(a, d, n);

	if (x == 1 or x == n - 1):
		return True;
	while (d != n - 1):
		x = (x * x) % n;
		d *= 2;
		if (x == 1):
			return False;
		if (x == n - 1):
			return True;
	# Return composite
	return False;

def isPrime(n, k):
	# Corner cases
	if (n <= 1 or n == 4):
		return False;
	if (n <= 3):
		return True;
	d = n - 1;
	while (d % 2 == 0):
		d //= 2;

	for i in range(k):
		if (millerTest(d, n) == False):
			return False;
	return True;

# k = 4;

# print("All primes smaller than 100: ");
# for n in range(1,100):
# 	if (isPrime(n, k)):
# 		print(n , end=" ");

