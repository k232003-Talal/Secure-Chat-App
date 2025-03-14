
PC1 = [
    57, 49, 41, 33, 25, 17,  9,
    1 , 58, 50, 42, 34, 26, 18,
    10, 2 , 59, 51, 43, 35, 27,
    19, 11, 3 , 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7 , 62, 54, 46, 38, 30, 22,
    14, 6 , 61, 53, 45, 37, 29,
    21, 13, 5 , 28, 20, 12,  4
]

PC2 = [
    14, 17, 11, 24, 1 ,  5,
    3 , 28, 15, 6 , 21, 10,
    23, 19, 12, 4 , 26,  8,
    16, 7 , 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

#Number of left shifts per round
SHIFT_ORDER = [
    1, 1, 2, 2, 2, 2, 2, 2,
    1, 2, 2, 2, 2, 2, 2, 1
]

def string_to_binary(input_string):
    """Converts string to a binary string."""
    return bin(int(input_string, 16))[2:].zfill(64)

def permute(key, table):
    """Permutates the key according to the given table."""
    return ''.join(key[i - 1] for i in table)

def left_shift(key_half, num_shifts):
    """Shifts the key half to the left by the given number of shifts."""
    return key_half[num_shifts:] + key_half[:num_shifts]

def generate_round_keys(key):
    """Generates the 16 round keys for DES."""
    # Apply PC-1 permutation, this will also apply the parity drop on the key.
    key_64bit = string_to_binary(key)
    
    permuted_key = permute(key_64bit, PC1)

    # Split the key into two 28-bit halves
    left_half = permuted_key[:28]
    right_half = permuted_key[28:]

    round_keys = []

    # Generate 16 round keys
    for shifts in SHIFT_ORDER:
        # Shift the halves
        left_half = left_shift(left_half, shifts)
        right_half = left_shift(right_half, shifts)

        combined_key = left_half + right_half

        # Apply PC-2 permutation to get the 48 bit round key
        round_key = permute(combined_key, PC2)
        round_keys.append(round_key)
        
    return round_keys

def main():
    key = "efeefdd"

    round_key = generate_round_keys(key)

    print(f"Original 64 Bit Key: {key}")

    for i in range(16):
        print(f'Round {i + 1} Key: {round_key[i]}')

if __name__ == "__main__":
    main()