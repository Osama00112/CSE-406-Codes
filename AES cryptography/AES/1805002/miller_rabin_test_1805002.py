import random

def modular_exponentiation(base, exponent, modulus):
    result = 1
    base = base % modulus
    
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        exponent = exponent // 2  
        base = (base * base) % modulus

    return result

def miller_rabin_test(difference, potential_prime):
    random_base = 2 + random.randint(1, potential_prime - 4)
    witness = modular_exponentiation(random_base, difference, potential_prime)

    if witness == 1 or witness == potential_prime - 1:
        return True

    while difference != potential_prime - 1:
        witness = (witness * witness) % potential_prime
        difference *= 2

        if witness == 1:
            return False
        if witness == potential_prime - 1:
            return True

    return False

def isPrime(candidate, num_trials):
    # Corner cases
    if candidate <= 1 or candidate == 4:
        return False
    if candidate <= 3:
        return True

    difference = candidate - 1
    while difference % 2 == 0:
        difference //= 2

    for _ in range(num_trials):
        if not miller_rabin_test(difference, candidate):
            return False

    return True
