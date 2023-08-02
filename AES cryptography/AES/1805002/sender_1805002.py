import socket			
import large_prime_1805002
import primitive_root_1805002
import AES_1805002

prime, factors = large_prime_1805002.generate_k_bit_prime_number(128)
phi_prime = prime - 1

g = primitive_root_1805002.generate_primitive_root(prime, factors)

a, _ = large_prime_1805002.generate_k_bit_prime_number(64)

A = primitive_root_1805002.exp_by_squaring_mod(g, a, prime)

s = socket.socket()		
print ("Socket successfully created")

port = 12345			

s.bind(('', port))		
print ("socket binded to %s" %(port))

# put the socket into listening mode
s.listen(5)	
print ("socket is listening")		

string_msg = "Here are the hex numbers p, g, and A"
hex_numbers = [hex(prime), hex(g), hex(A)]
data = string_msg + "%" + "&".join(hex_numbers)

#print(data)

# a forever loop until we interrupt it or
# an error occurs
while True:

    # Establish connection with client.
    c, addr = s.accept()	
    print ('Got connection from', addr )
    
    # send a thank you message to the client. encoding to send byte type.
    c.send(data.encode())
    
    # Receive the data from the client
    B_hex = c.recv(1024).decode()
    B = int(B_hex, 16)
    
    print(B)

    shared_key = primitive_root_1805002.exp_by_squaring_mod(B, a, prime)
    shared_key_hex = hex(shared_key)[2:]
    
    print("Shared Key:", shared_key)
    print("Shared Key in hex:", shared_key_hex)
    
    print("Ready for transmission")
    # Close the connection with the client
    
    #text = input("Plain Text:\nIn ASCII:")
    #padded_text, text_padding_count = AES.text_padding(text, 16)
    text = "Two One Nine Two Osama Haque"
    
    text_in_hex = text.encode().hex()
    print("In HEX:", text_in_hex)    

    aes_instance = AES_1805002.AES(shared_key_hex, 128)
    
    chunk_size = 16
    encrypted_chunks = []

    total_pad = 0
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        padded_chunk, pads = AES_1805002.text_padding(chunk, chunk_size)
        total_pad += pads
        #chunk_in_hex = padded_chunk.encode().hex()
        chunk_in_hex = padded_chunk.encode().hex()
        encrypted_chunk = aes_instance.cipher_text(chunk_in_hex)
        encrypted_chunks.append(encrypted_chunk)
   
    encrypted_data = "&".join(encrypted_chunks)
    data_with_pad = encrypted_data + "%" + str(total_pad)
    c.send(data_with_pad.encode())
    
    

    c.close()

    # Breaking once connection closed
    break
