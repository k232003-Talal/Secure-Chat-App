def calculate_sha1(input_message):
    # SHA-1 Standard Initial Hash Values
    initial_hash = {
        'h0': 0x67452301,
        'h1': 0xEFCDAB89,
        'h2': 0x98BADCFE,
        'h3': 0x10325476,
        'h4': 0xC3D2E1F0
    }
    
    # SHA-1 Round Constants
    ROUND_CONSTANTS = {
        'K1': 0x5A827999,  # For Round 0-19
        'K2': 0x6ED9EBA1,  # For Round 20-39
        'K3': 0x8F1BBCDC,  # For Round 40-59
        'K4': 0xCA62C1D6   # For Round 60-79
    }
    
    # Convert Message to Binary and add Padding
    padded_binary = pad_message(input_message)
    
    # Process Message in Chunks of 512 bits (64 bytes)
    for message_chunk in get_chunks(padded_binary, chunk_size=512):
        # Create and Extend Message Schedule (Word Array)
        message_schedule = create_message_schedule(message_chunk)
        
        # The Working Variables for this Chunk
        hash_values = initial_hash.copy()
        a, b, c, d, e = (hash_values['h0'], hash_values['h1'], 
                        hash_values['h2'], hash_values['h3'], 
                        hash_values['h4'])
        
        # Main SHA-1 Compression Function
        for i in range(80):
            if i <= 19:
                logical_func = (b & c) | ((~b) & d)
                constant = ROUND_CONSTANTS['K1']
            elif i <= 39:
                logical_func = b ^ c ^ d
                constant = ROUND_CONSTANTS['K2']
            elif i <= 59:
                logical_func = (b & c) | (b & d) | (c & d)
                constant = ROUND_CONSTANTS['K3']
            else:
                logical_func = b ^ c ^ d
                constant = ROUND_CONSTANTS['K4']
            
            # Calculate new Values
            temp = (rotate_left(a, 5) + logical_func + 
                   e + constant + message_schedule[i]) & 0xffffffff
            
            # Update Working Variables
            e = d
            d = c
            c = rotate_left(b, 30)
            b = a
            a = temp
        
        # Update Hash Values for this Chunk
        initial_hash['h0'] = (initial_hash['h0'] + a) & 0xffffffff
        initial_hash['h1'] = (initial_hash['h1'] + b) & 0xffffffff
        initial_hash['h2'] = (initial_hash['h2'] + c) & 0xffffffff
        initial_hash['h3'] = (initial_hash['h3'] + d) & 0xffffffff
        initial_hash['h4'] = (initial_hash['h4'] + e) & 0xffffffff
    
    # Concatenate Final Hash Values
    # %08x means the Number will be Converted to Hexadecimal with 8 Digits
    final_hash = '%08x%08x%08x%08x%08x' % (
        initial_hash['h0'], initial_hash['h1'], 
        initial_hash['h2'], initial_hash['h3'], 
        initial_hash['h4']
    )
    
    return final_hash

def pad_message(message):
    """
    Pad the Message According to SHA-1 Specifications:
    1. Convert to Binary
    2. Append '1' bit
    3. Append Zeros Until Length ≡ 448 (Length mod 512)
    4. Append 64-bit Message Length
    """
    # Convert Message to Binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    # Append '1' bit
    binary_message += '1'
    
    # Append Zeros Until Length ≡ 448 (Length mod 512)
    while len(binary_message) % 512 != 448:
        binary_message += '0'
    
    # Append 64-bit Message Length
    message_length = len(message) * 8
    binary_message += format(message_length, '064b')
    
    return binary_message

def get_chunks(message, chunk_size):
    """Split Message into Chunks of Specified size."""
    return [message[i:i + chunk_size] 
            for i in range(0, len(message), chunk_size)]

def create_message_schedule(chunk):
    """
    Create the Message Schedule (A Word Array) for SHA-1:
    1. Gets Input Chunk of Data
    2. Split chunk into 16 32-bit words
    3. Extend to 80 Words Using SHA-1 Algorithm
    4. Return the Message Schedule (Word Array)
    """
    # Convert Chunk Into Initial 16 Words
    words = [int(chunk[i:i + 32], 2) 
            for i in range(0, len(chunk), 32)]
    
    # Extending to 80 Words
    words.extend([0] * 64)
    
    # Filling Remaining Words Using SHA-1 Word Generation Algorithm
    for i in range(16, 80):
        new_word = words[i-3] ^ words[i-8] ^ words[i-14] ^ words[i-16]
        words[i] = rotate_left(new_word, 1)
    
    return words

def rotate_left(number, bits_to_rotate):
    """Perform a Circular left Rotation on a 32-bit Number."""
    return ((number << bits_to_rotate) | 
            (number >> (32 - bits_to_rotate))) & 0xffffffff # The & 0xffffffff is to Ensure the Number is 32 bits long
def main():
    test_message = "Hello, World"
    hash_result = calculate_sha1(test_message)

    print(f"Input message: {test_message}")
    print(f"SHA-1 hash: {hash_result}")

if __name__ == "__main__":
    main()