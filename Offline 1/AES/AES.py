import math
import numpy as np
import bitvector_demo
from BitVector import *
import time



class AES:
    key_size = 128
    rounds = 10
    dimension = 4
    state_matrix = None
    
    def __init__(self, key, key_size = 128):
        

        
        if key_size == 192:
            self.rounds = 12
            self.dimension = 6
        elif key_size == 256:
            self.rounds = 14
            self.dimension = 8

        self.key = self.text_to_matrix(key)
        init_time = time.time()
        self.round_keys = self.generate_round_keys(self.key)
        self.key_explansion_time = time.time() - init_time

            
    def round_constant(self, round_num):
        round_constants = [ 0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
                            0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
                            0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
                            0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39 ]
        return [round_constants[round_num], 0x00, 0x00, 0x00]
    
    def word_subs(self, w):
        for i in range(len(w)):
            byte_value = int(w[i], 16)  
            w[i] = format(bitvector_demo.Sbox[byte_value], '02x')  
        return w
            

    def word_subs_inverse(self, w):
        for i in range(len(w)):
            byte_value = int(w[i], 16)  
            w[i] = format(bitvector_demo.InvSbox[byte_value], '02x')  
        return w
            
    def text_to_matrix(self, text):
        byte_count = len(text) // 2              
        rows = cols = self.dimension
        
        matrix = np.zeros((rows, cols), dtype=object)
        
        for col in range(cols):
            start_index = col * rows * 2  
            for row in range(rows):
                byte_index = start_index + row * 2
                byte = text[byte_index:byte_index + 2]  
                matrix[col][row] = byte
        return matrix
    
    def matrix_to_text(self, matrix):
        rows, cols = matrix.shape
        text = ""
        for row in range(rows):
            for col in range(cols):
                text += matrix[row][col]
        return text
    
    def circular_left_shift_key(self, w):
        first_byte = w[0]
        length = len(w)
        for i in range (0, length):
            if i == (length - 1):
                w[i] = first_byte
            else:
                w[i] = w[i+1]
        return w     
    
    def circular_right_shift_key(self, w):
        last_byte = w[-1]
        length = len(w)
        for i in range(length - 1, -1, -1):
            if i == 0:
                w[i] = last_byte
            else:
                w[i] = w[i - 1]
        return w

    def process_row(self, row, round_num):
        shifted_row = self.circular_left_shift_key(row)
        substituted_row = self.word_subs(shifted_row)
        round_const = self.round_constant(round_num)
        xored_row = [format(int(substituted_row[i], 16) ^ round_const[i], '02x') for i in range(len(substituted_row))]
        return xored_row
                
    def generate_round_keys(self, matrix):
        round_keys = []
        round_keys.append(matrix.copy())
        dim = self.dimension
        
        #print("dimension is:", dim)

        for round_num in range(1, self.rounds + 1):
            target_row = matrix[-1]
            target_copy = target_row.copy()
            processed_row = self.process_row(target_row, round_num)

            new_matrix = matrix.copy()
            print("dimension:", len(new_matrix))
            for i in range(dim):
                new_matrix[0][i] = format(int(matrix[0][i], 16) ^ int(processed_row[i], 16), '02x')

            for j in range(1, dim):
                for i in range(dim):
                    if j == 3:
                        new_matrix[j][i] = format(int(new_matrix[j-1][i], 16) ^ int(target_copy[i], 16), '02x')
                    else:
                        new_matrix[j][i] = format(int(new_matrix[j-1][i], 16) ^ int(matrix[j][i], 16), '02x')
            matrix = new_matrix.copy()
            round_keys.append(matrix.copy())

        return round_keys
    
    def byte_subs(self, matrix, rows, cols):
        for i in range(rows):
            for j in range(cols):
                matrix[i][j] = format(
                    bitvector_demo.Sbox[int(matrix[i][j], 16)], '02x'
                )
                
    def inv_byte_subs(self, matrix, rows, cols):
        for i in range(rows):
            for j in range(cols):
                matrix[i][j] = format(
                    bitvector_demo.InvSbox[int(matrix[i][j], 16)], '02x'
                )

    def add_round_key(self, state_matrix, round_key_matrix):
        #new_state_matrix = state_matrix.copy()
        dim = self.dimension
        for i in range(dim):
            for j in range(dim):
                self.state_matrix[i][j] = format(
                    int(state_matrix[i][j], 16) ^ int(round_key_matrix[i][j], 16), '02x'
                )

    def shift_rows(self, state_matrix):
        state_matrix = np.transpose(state_matrix)  
        dim = self.dimension
        for i in range(1, dim):
            shift_amount = i
            state_matrix[i] = np.roll(state_matrix[i], -shift_amount)
        
        state_matrix = np.transpose(state_matrix)  
        
        return state_matrix

    def inv_shift_rows(self, state_matrix):
        state_matrix = np.transpose(state_matrix) 
        dim = self.dimension
        for i in range(1, dim):
            shift_amount = i
            state_matrix[i] = np.roll(state_matrix[i], shift_amount)

        state_matrix = np.transpose(state_matrix)  

        return state_matrix

            
    def mix_col(self, state_matrix):
        tmp = []
        modulus = BitVector(bitstring="100011011")

        for i in range(len(bitvector_demo.Mixer)):
            l = []
            for j in range(len(state_matrix[0])):
                bb = BitVector(intVal=0, size=8)
                for k in range(len(state_matrix)):
                    a = bitvector_demo.Mixer[j][k]
                    b = BitVector(intVal=int(state_matrix[i][k], 16), size=8)
                    ss = a.gf_multiply_modular(b, modulus, 8)
                    bb = bb ^ ss
                l.append(format(bb.intValue(), '02x'))  
                
            self.state_matrix[i] = l
            tmp.append(l)
            
    
    def inv_mix_col(self, state_matrix):
        tmp = []
        modulus = BitVector(bitstring="100011011")

        for i in range(len(bitvector_demo.InvMixer)):
            l = []
            for j in range(len(state_matrix[0])):
                bb = BitVector(intVal=0, size=8)
                for k in range(len(state_matrix)):
                    a = bitvector_demo.InvMixer[j][k]
                    b = BitVector(intVal=int(state_matrix[i][k], 16), size=8)
                    ss = a.gf_multiply_modular(b, modulus, 8)
                    bb = bb ^ ss
                l.append(format(bb.intValue(), '02x'))  

            self.state_matrix[i] = l
            tmp.append(l)

    def cipher_text(self, text):
        self.state_matrix = self.text_to_matrix(text)
        round_count = 0
        self.add_round_key(self.state_matrix, self.round_keys[round_count])
        round_count += 1
        dim = self.dimension
        for i in range(1, self.rounds):
            self.byte_subs(self.state_matrix, dim, dim)
            self.shift_rows(self.state_matrix)
            self.mix_col(self.state_matrix)
            self.add_round_key(self.state_matrix, self.round_keys[round_count])
            round_count += 1
        self.byte_subs(self.state_matrix, dim, dim)
        self.shift_rows(self.state_matrix)
        self.add_round_key(self.state_matrix, self.round_keys[round_count])
        round_count += 1
        
        return self.matrix_to_text(self.state_matrix)
    
    def decipher_text(self, text):
        self.state_matrix = self.text_to_matrix(text)
        round_count = self.rounds
        self.add_round_key(self.state_matrix, self.round_keys[round_count])
        round_count -= 1
        dim = self.dimension

        for i in range(self.rounds - 1, 0, -1):
            self.inv_shift_rows(self.state_matrix)
            self.inv_byte_subs(self.state_matrix, dim, dim)
            self.add_round_key(self.state_matrix, self.round_keys[round_count])

            self.inv_mix_col(self.state_matrix)      
            round_count -= 1

        self.inv_shift_rows(self.state_matrix)
        self.inv_byte_subs(self.state_matrix, dim, dim)
        self.add_round_key(self.state_matrix, self.round_keys[round_count])
        
        return self.matrix_to_text(self.state_matrix)


def key_padding(key):
    pad_length = 0
    length = len(key)
    #print ("length is:", length)
    if length == 16:
        return key, 16, 0
    elif length < 16:
        pad_length = 16 - length
        return key.ljust(16, '0'), 16, pad_length
    else:
        # extend to the nearest multiple of 8
        if length % 8 == 0:
            multiple = length // 8
        else:
            multiple = (length // 8) + 1
        multiple *= 8
        
        pad_length = multiple - length
        return key.ljust(multiple, '0'), multiple, pad_length
    
def text_padding(text):
    pad_length = 0
    length = len(text)
    if length == 16:
        return text, 0
    elif length < 16:
        pad_length = 16 - length
        return text.ljust(16, '0'), pad_length
    else:
        # extend to the nearest multiple of 8
        if length % 8 == 0:
            multiple = length // 8
        else:
            multiple = (length // 8) + 1
        multiple *= 8
        
        pad_length = multiple - length
        return text.ljust(multiple, '0'), pad_length
        

if __name__ == "__main__":
    #text = input("Plain Text:\nIn ASCII:")
    text = "Two One Nine Two one more down one more to go"
    padded_text, text_padding_count = text_padding(text)
    #print(padded_text)
    
    text_in_hex = padded_text.encode().hex()
    print("In HEX:", text_in_hex)
    #print("len:", len(text_in_hex))
    
    #key = input("\nKey:\nIn ASCII:")
    key = "Thats my Kung Fu and osm"
    padded_key, multiple, key_padding_count = key_padding(key)
    print("multiple:", multiple)
    key_in_hex = key.encode().hex()
    print("In HEX:", key_in_hex)
    
    
    
    aes_instance = AES(key_in_hex, multiple * 8)
    encrypted_text = aes_instance.cipher_text(text_in_hex)
    
    #chunk_size = len(key_in_hex)
    chunk_size = multiple
    encrypted_chunks = []
    
    # print("Cipher Text:\nIn HEX:")
    # print(encrypted_text)
    # #matrix = aes_instance.text_to_matrix(key_in_hex)
    # decrypted_text = aes_instance.decipher_text(encrypted_text)
    # print("Deciphered Text:\nIn HEX:")
    # print(decrypted_text)
    
    # deciphered_ascii = ''.join([chr(int(decrypted_text[i:i+2], 16)) for i in range(0, len(decrypted_text), 2)])
    # print("In ASCII:")
    # print(deciphered_ascii)    
    
    print("chunk size:", chunk_size)

    
    for i in range(0, len(padded_text), chunk_size):
        chunk = padded_text[i:i + chunk_size]
        print("chunk is:", chunk)
        #padded_chunk = text_padding(chunk)
        #chunk_in_hex = padded_chunk.encode().hex()
        chunk_in_hex = chunk.encode().hex()
        encrypted_chunk = aes_instance.cipher_text(chunk_in_hex)
        encrypted_chunks.append(encrypted_chunk)

    print("Ciphered Chunks:\nIn HEX:")
    for chunk in encrypted_chunks:
        print(chunk)

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
    deciphered_text = deciphered_text[:-text_padding_count]
    print("Deciphered Text:\nIn ASCII:")
    print(deciphered_text)
    