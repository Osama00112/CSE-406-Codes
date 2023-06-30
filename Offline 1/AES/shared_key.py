import large_prime
import primitive_root
import time

prime, factors = large_prime.generate_k_bit_prime_number(128)
phi_prime = prime - 1

g = primitive_root.generate_primitive_root(prime, factors)

# now available g and prime

a, _ = large_prime.generate_k_bit_prime_number(64)
b, _ = large_prime.generate_k_bit_prime_number(64)

A = primitive_root.exp_by_squaring_mod(g, a, prime)
B = primitive_root.exp_by_squaring_mod(g, b, prime)


received1 = primitive_root.exp_by_squaring_mod(B, a, prime)
received2 = primitive_root.exp_by_squaring_mod(A, b, prime)

# print(received1)

# print(received2)

total_time_p = 0
total_time_g = 0
total_time_a = 0
total_time_A = 0
total_time_shared_key = 0

for i in range (10):
    init_time = time.time()
    prime, factors = large_prime.generate_k_bit_prime_number(128)
    time_for_p = time.time() - init_time
    
    total_time_p += time_for_p
    
    init_time = time.time()
    g = primitive_root.generate_primitive_root(prime, factors)
    time_for_g = time.time() - init_time
    
    total_time_g += time_for_g
    
    init_time = time.time()
    a, _ = large_prime.generate_k_bit_prime_number(64)
    time_for_a = time.time() - init_time    
    
    total_time_a += time_for_a
    
    b, _ = large_prime.generate_k_bit_prime_number(64)
    
    init_time = time.time()
    A = primitive_root.exp_by_squaring_mod(g, a, prime)
    time_for_A = time.time() - init_time    
    
    total_time_A += time_for_A
    
    B = primitive_root.exp_by_squaring_mod(g, b, prime)
    
    init_time = time.time()
    received1 = primitive_root.exp_by_squaring_mod(B, a, prime)
    time_for_shared_key = time.time() - init_time    
    
    total_time_shared_key += time_for_shared_key
    
    received2 = primitive_root.exp_by_squaring_mod(A, b, prime)
    
avg_p = total_time_p / 10
avg_g = total_time_g / 10
avg_a = total_time_a / 10
avg_A = total_time_A / 10
avg_shared_key = total_time_shared_key / 10

print("Avg time for p: ", avg_p, " sec")
print("Avg time for g: ", avg_g, " sec")
print("Avg time for a: ", avg_a, " sec")
print("Avg time for A: ", avg_A, " sec")
print("Avg time for shared key: ", avg_shared_key, " sec")
