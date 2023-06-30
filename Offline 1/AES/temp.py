import bitvector_demo

def convert_to_hex(string):
    hex_code = string.encode().hex()  
    hex_code = hex_code.ljust(32, '0')
    
    w = []

    for i in range(0, len(hex_code), 8):
        word = hex_code[i:i+8]
        word_values = []
        
        for j in range(0, len(word), 2):
            byte = word[j:j+2]
            #value = int(byte, 16)
            word_values.append(byte)

        w.append(word_values)
    
    return w


def circular_left_shift(w, word_index):
    first_byte = w[word_index][0]
    length = len(w[word_index])
    for i in range (0, length):
        if i == (length - 1):
            w[word_index][i] = first_byte
        else:
            w[word_index][i] = w[word_index][i+1]
    return w     

# Take user input
input_string = input("Enter a string: ")

# Convert string to hex code and divide into four words
result = convert_to_hex(input_string)

# Print the four words
print("w[0] =", result[0])
print("w[1] =", result[1])
print("w[2] =", result[2])
print("w[3] =", result[3])

result = circular_left_shift(result, 0)
print("after lshift")
# Print the four words
print("w[0] =", result[0])
print("w[1] =", result[1])
print("w[2] =", result[2])
print("w[3] =", result[3])

# Substitute bytes with values from Sbox
substituted_word = []
for byte in result[3]:
    substituted_byte = bitvector_demo.Sbox[int(byte, 16)]
    substituted_word.append(substituted_byte)

result[3] = substituted_word

print("after substitution")
# Print the four words
print("w[0] =", result[0])
print("w[1] =", result[1])
print("w[2] =", result[2])
print("w[3] =", result[3])
