#pip install sympy (install if you havent already)
import math
import random

from sympy import primerange

PRIMES_LIST : list = list(primerange(100))

def generate_keypair(list_p: list = PRIMES_LIST):
    """
    Generate public and private keys for RSA encryption.
    
    Args:
    p (int): A large prime number
    q (int): Another large prime number
    
    Returns:
    tuple: ((public_key, n), (private_key, n))
    """
    # Generate Prime Numbers
    p = list_p[random.randint(0, len(list_p) - 1)]
    q = list_p[random.randint(0, len(list_p) - 1)]
    while q == p:
        q = list_p[random.randint(0, len(list_p))]
    
    # Compute n (modulus)
    n = p * q
    
    # Compute phi(n)
    phi = (p - 1) * (q - 1)
    
    # Choose e (public key exponent)
    e = random.randrange(1, phi)
    while math.gcd(e, phi) != 1:
        e = random.randrange(1, phi)
    
    # Compute d (private key exponent)
    # d is the modular multiplicative inverse of e
    def extended_euclidean(a, b):
        """Extended Euclidean Algorithm to find modular multiplicative inverse."""
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = extended_euclidean(b % a, a)
            return gcd, y - (b // a) * x, x
    
    _, d, _ = extended_euclidean(e, phi)
    
    # Ensure d is positive
    d = d % phi
    
    # Public key is (e, n), private key is (d, n)
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    """
    Encrypt a message using the public key.
    
    Args:
    public_key (tuple): (e, n)
    plaintext (str): Message to encrypt
    
    Returns:
    list: Encrypted message as list of integers
    """
    e, n = public_key
    # Convert each character to its ASCII value and encrypt
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

def decrypt(private_key, ciphertext):
    """
    Decrypt a message using the private key.
    
    Args:
    private_key (tuple): (d, n)
    ciphertext (list): Encrypted message as list of integers
    
    Returns:
    str: Decrypted message
    """
    d, n = private_key
    # Decrypt each number back to its character
    
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)

# Example usage
def main():
    # Generate public and private keys
    public_key, private_key = generate_keypair(PRIMES_LIST)
    
    print("Public key:", public_key)
    print("Private key:", private_key)
    
    # Message to encrypt
    message = "Hello, RSA Encryption!"
    print("\nOriginal message:", message)
    
    # Encrypt the message
    encrypted_msg = encrypt(public_key, message)
    print("Encrypted message:", encrypted_msg)
    
    # Decrypt the message
    decrypted_msg = decrypt(private_key, encrypted_msg)
    print("Decrypted message:", decrypted_msg)

if __name__ == "__main__":
    main()