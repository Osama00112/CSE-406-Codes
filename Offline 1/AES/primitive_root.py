import miller_rabin_test

def exp_by_squaring_mod(x, n, p):
    if n < 0:
        return exp_by_squaring_mod(pow(x, -1, p), -n, p)
    elif n == 0:
        return 1 % p
    elif n % 2 == 0:
        return exp_by_squaring_mod((x * x) % p, n // 2, p)
    else:
        return (x * exp_by_squaring_mod((x * x) % p, (n - 1) // 2, p)) % p


def generate_primitive_root(prime, factors):
    min_value = 2
    max_value = 10000
    g = min_value
    factor_count = len(factors)
    phi_prime = prime - 1
    
    while(True):
        mod_value = []
        
        # populating list of results of phi/factors
        for i in range(factor_count):
            div = phi_prime // factors[i] 
            # Calculate: g^div (mod prime)
            mod_value.append(exp_by_squaring_mod(g, div, prime))
            
        
        is_primitive_root = True
        
        # checking all values
        for value in mod_value:
            # if any value is 1, g cannot be a primitive root. jump to next candidate
            if value == 1:
                
                is_primitive_root = False
                # searching for next candidate
                while True:
                    # jumping to next integer
                    g += 1
                    
                    # if g exceeds max value, just return a prime number in the range
                    if g > max_value:
                        g = min_value
                        while True:
                            if miller_rabin_test.isPrime(g, 4):
                                return g
                            g += 1
                            
                    # if g is prime, we found a candidate, stop jumping for g (break) and proceed with primitive checking
                    if miller_rabin_test.isPrime(g, 4):
                        break
                # g is not prime, continue searching for g
            
            # found candidate as previous g failed. dont need to check other values. break
            break
        
        # if it is potential g, break
        if is_primitive_root:
            break
        # else continue searching
        else:
            continue
            

    return g
    
