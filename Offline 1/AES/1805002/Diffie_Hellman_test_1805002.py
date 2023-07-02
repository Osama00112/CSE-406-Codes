import large_prime_1805002
import primitive_root_1805002
import time

#bit_count = int(input("Size of the key(Bits):"))
#iteration = int(input("Number of iterations for performance analysis:"))

bit_counts = [128, 192, 256]
iteration = 1

list_for_p = []
list_for_g = []
list_for_a = []
list_for_A = []
list_for_key = []
    
for j in range(3):
    # prime, factors = large_prime_1805002.generate_k_bit_prime_number(bit_counts[i])

    # g = primitive_root_1805002.generate_primitive_root(prime, factors)

    # # now available g and prime

    # half_bit_count = bit_counts[i] // 2

    # a, _ = large_prime_1805002.generate_k_bit_prime_number(half_bit_count)
    # b, _ = large_prime_1805002.generate_k_bit_prime_number(half_bit_count)

    # A = primitive_root_1805002.exp_by_squaring_mod(g, a, prime)
    # B = primitive_root_1805002.exp_by_squaring_mod(g, b, prime)


    # received1 = primitive_root_1805002.exp_by_squaring_mod(B, a, prime)
    # received2 = primitive_root_1805002.exp_by_squaring_mod(A, b, prime)

    # print("B^a (mod prime):",received1)
    # print("A^b (mod prime):",received2)


    
    total_time_p = 0
    total_time_g = 0
    total_time_a = 0
    total_time_A = 0
    total_time_shared_key = 0

    for i in range (iteration):
        init_time = time.time()
        prime, factors = large_prime_1805002.generate_k_bit_prime_number(bit_counts[j])
        time_for_p = time.time() - init_time
        
        half_bit_count = bit_counts[j] // 2
        
        total_time_p += time_for_p
        
        init_time = time.time()
        g = primitive_root_1805002.generate_primitive_root(prime, factors)
        time_for_g = time.time() - init_time
        
        total_time_g += time_for_g
        
        init_time = time.time()
        a, _ = large_prime_1805002.generate_k_bit_prime_number(half_bit_count)
        time_for_a = time.time() - init_time    
        
        total_time_a += time_for_a
        
        b, _ = large_prime_1805002.generate_k_bit_prime_number(half_bit_count)
        
        init_time = time.time()
        A = primitive_root_1805002.exp_by_squaring_mod(g, a, prime)
        time_for_A = time.time() - init_time    
        
        total_time_A += time_for_A
        
        B = primitive_root_1805002.exp_by_squaring_mod(g, b, prime)
        
        init_time = time.time()
        received1 = primitive_root_1805002.exp_by_squaring_mod(B, a, prime)
        time_for_shared_key = time.time() - init_time    
        
        total_time_shared_key += time_for_shared_key
        
        received2 = primitive_root_1805002.exp_by_squaring_mod(A, b, prime)
        
    avg_p = total_time_p / iteration
    avg_g = total_time_g / iteration
    avg_a = total_time_a / iteration
    avg_A = total_time_A / iteration
    avg_shared_key = total_time_shared_key / iteration

    print("\nAvg time for p:", avg_p, "seconds")
    print("Avg time for g:", avg_g, "seconds")
    print("Avg time for a:", avg_a, "seconds")
    print("Avg time for A:", avg_A, "seconds")
    print("Avg time for shared key:", avg_shared_key, "seconds\n")
    
    list_for_p.append("{:.7f}".format(avg_p))
    list_for_g.append("{:.7f}".format(avg_g))
    list_for_a.append("{:.7f}".format(avg_a))
    list_for_A.append("{:.7f}".format(avg_A))
    list_for_key.append("{:.7f}".format(avg_shared_key))
    
print("--------------------------------------------------------------------------\n")
print("|       |               Computation Time For                             |\n")
print("|   k   |----------------------------------------------------------------|\n")
print("|       |    p       |      g     |      a     |      A     | shared key |\n")
print("--------------------------------------------------------------------------\n")
print("|  128  | ", list_for_p[0] ," | ", list_for_g[0] ," | ", list_for_a[0] ," | ", list_for_A[0] ," | ", list_for_key[0] ," |\n")
print("--------------------------------------------------------------------------")
print("|  192  | ", list_for_p[1] ," | ", list_for_g[1] ," | ", list_for_a[1] ," | ", list_for_A[1] ," | ", list_for_key[1] ," |\n")
print("--------------------------------------------------------------------------")
print("|  256  | ", list_for_p[2] ," | ", list_for_g[2] ," | ", list_for_a[2] ," | ", list_for_A[2] ," | ", list_for_key[2] ," |\n")
print("--------------------------------------------------------------------------")
    
