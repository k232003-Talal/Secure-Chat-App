from des_key_gen import generate_round_keys


def initial_permutation(input_block):
    """Apply the Initial Permutation Table to the 64-bit Block"""
    INITIAL_PERM_TABLE = [58, 50, 42, 34, 26, 18, 10, 2,
                         60, 52, 44, 36, 28, 20, 12, 4,
                         62, 54, 46, 38, 30, 22, 14, 6,
                         64, 56, 48, 40, 32, 24, 16, 8,
                         57, 49, 41, 33, 25, 17, 9, 1,
                         59, 51, 43, 35, 27, 19, 11, 3,
                         61, 53, 45, 37, 29, 21, 13, 5,
                         63, 55, 47, 39, 31, 23, 15, 7]
    return ''.join(input_block[position-1] for position in INITIAL_PERM_TABLE)

def final_permutation(input_block):
    """Apply the Final Permutation to the 64-bit Block"""
    FINAL_PERM_TABLE = [40, 8, 48, 16, 56, 24, 64, 32,
                       39, 7, 47, 15, 55, 23, 63, 31,
                       38, 6, 46, 14, 54, 22, 62, 30,
                       37, 5, 45, 13, 53, 21, 61, 29,
                       36, 4, 44, 12, 52, 20, 60, 28,
                       35, 3, 43, 11, 51, 19, 59, 27,
                       34, 2, 42, 10, 50, 18, 58, 26,
                       33, 1, 41, 9, 49, 17, 57, 25]
    return ''.join(input_block[position-1] for position in FINAL_PERM_TABLE)

def expansion(input_block):
    """Expand 32-bit Block to 48 bits Using the Expansion Table"""
    EXPANSION_TABLE = [32, 1, 2, 3, 4, 5,
                      4, 5, 6, 7, 8, 9,
                      8, 9, 10, 11, 12, 13,
                      12, 13, 14, 15, 16, 17,
                      16, 17, 18, 19, 20, 21,
                      20, 21, 22, 23, 24, 25,
                      24, 25, 26, 27, 28, 29,
                      28, 29, 30, 31, 32, 1]
    return ''.join(input_block[position-1] for position in EXPANSION_TABLE)

def permutation(input_block):
    """Apply Permutation to 32-bit Block"""
    PERMUTATION_TABLE = [16, 7, 20, 21, 29, 12, 28, 17,
                        1, 15, 23, 26, 5, 18, 31, 10,
                        2, 8, 24, 14, 32, 27, 3, 9,
                        19, 13, 30, 6, 22, 11, 4, 25]
    return ''.join(input_block[position-1] for position in PERMUTATION_TABLE)

def sbox_substitution(expanded_block):
    """Apply S-box Substitution to 48-bit Block to get 32-bit Output"""
    SUBSTITUTION_BOXES = [
        # S1
        [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
        # S2
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
        # S3
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
        # S4
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
        # S5
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
        # S6
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
        # S7
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
        # S8
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
    ]
    
    substitution_result = ""
    for box_index in range(8):
        current_chunk = expanded_block[box_index*6:(box_index+1)*6]
        row_number = int(current_chunk[0] + current_chunk[5], 2)
        column_number = int(current_chunk[1:5], 2)
        substitution_value = SUBSTITUTION_BOXES[box_index][row_number][column_number]
        substitution_result += format(substitution_value, '04b')
    return substitution_result

def f_function(right_half_block, current_round_key):
    """Implement the F-Function of DES"""
    # Expand Right half from 32 to 48 bits
    expanded_block = expansion(right_half_block)
    
    # XOR with Round key
    xored_block = ''.join(str(int(bit_a, 2) ^ int(bit_b, 2)) 
                         for bit_a, bit_b in zip(expanded_block, current_round_key))
    
    # S-box Substitution
    substituted_block = sbox_substitution(xored_block)
    
    # Permutation
    return permutation(substituted_block)

def string_to_binary(input_text):
    """Convert ASCII String to Binary String"""
    return ''.join(format(ord(char), '08b') for char in input_text)

def binary_to_Hex_string(binary_text):
    """Convert Binary String to ASCII String, Padding if Necessary"""
    # Pad the Binary String with Leading Zeros
    padding_length = (4 - len(binary_text) % 4) % 4
    padded_binary_text = ('0' * padding_length) + binary_text
    
    # Convert the Padded Binary String to HEX
    return ''.join(hex(int(padded_binary_text[index:index+4], 2))[2:]
                   for index in range(0, len(padded_binary_text), 4))

def pad_text(input_text):
    """Pad text to be Multiple of 8 bytes (64 bits)
       Also, put the Length of the Padding as the Padding to the Text
    """
    padding_length = 8 - (len(input_text) % 8)
    return input_text + chr(padding_length) * padding_length

def des_encrypt_block(plaintext_block, encryption_key):
    """
    Encrypt a 64-bit Block Using DES
    -Returns the Encrypted Block as a String of 64 bits
    """
    # Generate Round Keys
    round_keys = generate_round_keys(encryption_key)
    
    # Initial Permutation
    permuted_block = initial_permutation(plaintext_block)
    
    # Split into Left and Right Halves
    left_half = permuted_block[:32]
    right_half = permuted_block[32:]
    
    # 16 Rounds of Encryption
    for round_number in range(16):
        new_right_half = f_function(right_half, round_keys[round_number])
        new_right_half = ''.join(str(int(bit_a) ^ int(bit_b)) 
                                for bit_a, bit_b in zip(left_half, new_right_half))
        left_half = right_half
        right_half = new_right_half
    
    # Final swap of Left and Right Halves
    pre_final_block = right_half + left_half
    
    # Final Permutation
    return final_permutation(pre_final_block)

def des_encrypt_message(input_message, encryption_key):
    """
    Encrypt a Message Using DES(ECB Mode)
    -Returns Binary String of Encrypted Message
    """
    # Pad Message
    padded_message = pad_text(input_message)
    
    # Convert to Binary
    binary_message = string_to_binary(padded_message)
    
    # Encrypt each 64-bit Block
    encrypted_text = ""
    for block_start in range(0, len(binary_message), 64):
        current_block = binary_message[block_start:block_start+64]
        encrypted_block = des_encrypt_block(current_block, encryption_key)
        encrypted_text += encrypted_block
    
    return binary_to_Hex_string(encrypted_text)

def des_decrypt_block(ciphertext_block, decryption_key):
    """
    Decrypt a 64-bit Block Using DES
    - Returns the Decrypted Block as a String of 64 bits
    """
    # Generate Round Keys (same as encryption)
    round_keys = generate_round_keys(decryption_key)

    # Initial Permutation
    permuted_block = initial_permutation(ciphertext_block)

    # Split into Left and Right Halves
    left_half = permuted_block[:32]
    right_half = permuted_block[32:]

    # 16 Rounds of Decryption (reversed order of round keys)
    for round_number in range(15, -1, -1):
        new_right_half = f_function(right_half, round_keys[round_number])
        new_right_half = ''.join(str(int(bit_a) ^ int(bit_b))
                                     for bit_a, bit_b in zip(left_half, new_right_half))
        left_half = right_half
        right_half = new_right_half

    # Final swap of Left and Right Halves
    pre_final_block = right_half + left_half

    # Final Permutation
    return final_permutation(pre_final_block)

def des_decrypt_message(ciphertext, decryption_key):
    """
    Decrypt a Message Using DES
    - Returns the Decrypted Message as a String
    """
    # Convert Hexadecimal Ciphertext to Binary
    binary_ciphertext = ''.join(format(int(c, 16), '04b') for c in ciphertext)

    # Decrypt each 64-bit Block
    decrypted_binary = ""
    for block_start in range(0, len(binary_ciphertext), 64):
        current_block = binary_ciphertext[block_start:block_start+64]
        decrypted_block = des_decrypt_block(current_block, decryption_key)
        decrypted_binary += decrypted_block

    # Convert Binary to ASCII String
    decrypted_text = ""
    for i in range(0, len(decrypted_binary), 8):
        char_code = int(decrypted_binary[i:i+8], 2)
        decrypted_text += chr(char_code)

    # Remove PKCS7 padding
    if decrypted_text:
        padding_length = ord(decrypted_text[-1])
        # Validate padding
        if 1 <= padding_length <= 8:
            is_valid_padding = all(
                ord(decrypted_text[-(i+1)]) == padding_length 
                for i in range(padding_length)
            )
            if is_valid_padding:
                decrypted_text = decrypted_text[:-padding_length]

    return decrypted_text

def main():
    encrypted_text = des_encrypt_message("Amount: 75000", "12345678")
    print(f"Encrypted Text: {encrypted_text}")
    decrypted_text = des_decrypt_message(encrypted_text, "12345678")
    print(f"Decrypted Text: {decrypted_text}")
    

if __name__ == "__main__":
    main()
