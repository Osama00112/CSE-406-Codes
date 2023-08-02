import miller_rabin_test_1805002
import random

def generate_primes(prime_count, k, random_bit_count):
    primes = []
    while len(primes) < prime_count:
        n = random.getrandbits(random_bit_count)
        if miller_rabin_test_1805002.isPrime(n, k):
            primes.append(n)
    return primes


def generate_potential_factors(primes, sample_count):
    potential_factors = random.sample(primes, sample_count)
    potential_factors.append(2)
    return potential_factors

def generate_potential_prime(potential_factors):
    candidate_prime = 1
    for factor in potential_factors:
        candidate_prime *= factor
    candidate_prime += 1
    return candidate_prime

    
def is_k_bit(candidate_prime, k):
    return candidate_prime.bit_length() == k

def generate_k_bit_prime_number(k):
    accuracy_level = 4
    primes = generate_primes(1000, accuracy_level, 32)
    sample_count = k // 32

    potential_prime = None
    potential_factors = None
    
    while True:
        current_potential_factors = generate_potential_factors(primes, sample_count)
        current_prime = generate_potential_prime(current_potential_factors)
        if not is_k_bit(current_prime, k):
            continue
        if miller_rabin_test_1805002.isPrime(current_prime, accuracy_level):
            potential_prime = current_prime
            potential_factors = current_potential_factors
            break

    #print("Generated k-bit prime number:", potential_prime)
    return potential_prime, potential_factors

# def generate_k_by_2_bit_prime_number(k):
#     accuracy_level = 4
#     primes = generate_primes(1000, accuracy_level, 16)
#     sample_count = k // 32
#     k_by_2 = k // 2
    
#     potential_prime = None
#     potential_factors = None
    
#     while True:
#         current_potential_factors = generate_potential_factors(primes, sample_count)
#         current_prime = generate_potential_prime(current_potential_factors)
#         if not is_k_bit(current_prime, k_by_2):
#             continue
#         if miller_rabin_test.isPrime(current_prime, accuracy_level):
#             potential_prime = current_prime
#             potential_factors = current_potential_factors
#             break

#     print("Generated k/2-bit prime number:", potential_prime)
#     return potential_prime, potential_factors
