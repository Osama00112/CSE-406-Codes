import large_prime_1805002
import primitive_root_1805002
import time


prime, factors = large_prime_1805002.generate_k_bit_prime_number(128)

g = primitive_root_1805002.generate_primitive_root2(prime, factors, 104, 1000)

print(g)
# now available g and prime

half_bit_count = 128 // 2

a, _ = large_prime_1805002.generate_k_bit_prime_number(half_bit_count)
b, _ = large_prime_1805002.generate_k_bit_prime_number(half_bit_count)

A = primitive_root_1805002.exp_by_squaring_mod(g, a, prime)
B = primitive_root_1805002.exp_by_squaring_mod(g, b, prime)


received1 = primitive_root_1805002.exp_by_squaring_mod(B, a, prime)
received2 = primitive_root_1805002.exp_by_squaring_mod(A, b, prime)

print("B^a (mod prime):",received1)
print("A^b (mod prime):",received2)

