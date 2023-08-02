import AES_1805002
import time

if __name__ == "__main__":
    text = input("Plain Text:\nIn ASCII:")
    #text = "Two One Nine Two one more down one more to goabcde"
    #padded_text, text_padding_count = AES.text_padding(text, 16)
    #print(text)
    text_in_hex = text.encode().hex()
    print("In HEX:", text_in_hex)
    
    key = input("\nKey:\nIn ASCII:")
    #key = "Thats Kung Fu"
    padded_key, multiple, key_padding_count = AES_1805002.key_padding(key)

    key_in_hex = key.encode().hex()
    print("In HEX:", key_in_hex)
    

    aes_instance = AES_1805002.AES(key_in_hex, multiple * 8)
    encrypted_text = aes_instance.cipher_text(text_in_hex)

    chunk_size = multiple
    encrypted_chunks = []
    
    total_pad = 0
    start_time = time.time()
    
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        padded_chunk, pads = AES_1805002.text_padding(chunk, chunk_size)
        total_pad += pads
        chunk_in_hex = padded_chunk.encode().hex()
        encrypted_chunk = aes_instance.cipher_text(chunk_in_hex)
        encrypted_chunks.append(encrypted_chunk)

    encryption_time = time.time() - start_time
    # print("\nCiphered Text:\nIn HEX:")
    # for chunk in encrypted_chunks:
    #     print(chunk)
        
        
    encrypted_text_hex = ''.join(encrypted_chunks)
    print("\nCiphered Text:\nIn HEX:", encrypted_text_hex)
        
    encrypted_text_ascii = ''.join([chr(int(encrypted_text_hex[i:i + 2], 16)) for i in range(0, len(encrypted_text_hex), 2)])

    print("In ASCII:", encrypted_text_ascii)

    decrypted_chunks = []
    chunk_count = len(encrypted_chunks)
    i = 0
    
    start_time = time.time()
    for encrypted_chunk in encrypted_chunks:
        decrypted_chunk = aes_instance.decipher_text(encrypted_chunk)
        decrypted_chunks.append(decrypted_chunk)
    decryption_time = time.time() - start_time
    
    # print("Deciphered Chunks:\nIn HEX:")
    # for chunk in decrypted_chunks:
    #     print(chunk)
    
    decrypted_text_hex = ''.join(decrypted_chunks)
    deciphered_text_ascii = ''.join([chr(int(chunk[i:i + 2], 16)) for chunk in decrypted_chunks for i in range(0, len(chunk), 2)])
    
    if total_pad > 0:
        deciphered_text_ascii = deciphered_text_ascii[:-total_pad]
    else:
        deciphered_text_ascii = deciphered_text_ascii

    print("\nDeciphered Text:\nIn Hex:", decrypted_text_hex)
    print("In ASCII:", deciphered_text_ascii)
    
    print("\nExecution Time Details:")
    print("Key Scheduling:", aes_instance.key_explansion_time, "seconds")
    print("Encryption Time:", encryption_time, "seconds")
    print("Decryption Time:", decryption_time, "seconds\n")