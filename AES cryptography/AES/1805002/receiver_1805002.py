import socket
import large_prime_1805002
import primitive_root_1805002
import AES_1805002

b, _ = large_prime_1805002.generate_k_bit_prime_number(64)

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 12345

# Connect to the server on the local computer
s.connect(('127.0.0.1', port))

# Receive data from the server as a string
data = s.recv(1024).decode()

# Split the received data using the delimiters
delimiter1 = "%"
delimiter2 = "&"
string_msg, hex_numbers = data.split(delimiter1)[0], data.split(delimiter1)[1].split(delimiter2)

print("Received message:", string_msg)
print("Received hex numbers:", hex_numbers)

hex_values = [int(hex_num, 16) for hex_num in hex_numbers]

print("Hex values:", hex_values)

prime = hex_values[0]
g = hex_values[1]
A = hex_values[2]

B = primitive_root_1805002.exp_by_squaring_mod(g, b, prime)


B_hex = hex(B)


s.send(B_hex.encode())

shared_key = primitive_root_1805002.exp_by_squaring_mod(A, b, prime)
shared_key_hex = hex(shared_key)[2:]

print("Shared Key:", shared_key)
print("Shared Key in hex:", shared_key_hex)

print("Ready for transmission")

aes_instance = AES_1805002.AES(shared_key_hex, 128)

# code for receiving chunks
# Receive the encrypted chunks from the server
data_with_pad = s.recv(1024).decode()
encrypted_data, total_pad = data_with_pad.split(delimiter1)[0], int(data_with_pad.split(delimiter1)[1])
print("Total pad:", total_pad)   

encrypted_chunks = encrypted_data.split(delimiter2)


decrypted_chunks = []
chunk_count = len(encrypted_chunks)
i = 0
for encrypted_chunk in encrypted_chunks:
    decrypted_chunk = aes_instance.decipher_text(encrypted_chunk)
    decrypted_chunks.append(decrypted_chunk)

print("Deciphered Chunks:\nIn HEX:")
for chunk in decrypted_chunks:
    print(chunk)

deciphered_text = ''.join([chr(int(chunk[i:i + 2], 16)) for chunk in decrypted_chunks for i in range(0, len(chunk), 2)])
# deciphered_text = deciphered_text[:-text_padding_count]
print(deciphered_text)
if total_pad > 0:
    deciphered_text = deciphered_text[:-total_pad]
else:
    deciphered_text = deciphered_text
print("text padding count:", total_pad)
print("Deciphered Text:\nIn ASCII:")
print(deciphered_text)


# Close the connection
s.close()
