import design
import des
import rsa
import sha1
from filing import get_Private_key,get_Public_key,get_other_Username

#DES (for chat encrption)------------------------------------------------------------------------------------------------------------------- 

def set_des_key():
   with open(design.key_file_path, 'r') as file:
    key_des = file.read()
    return  key_des

def decrypt_message(msg):
   key_des=set_des_key()
   decrypted_msg=des.des_decrypt_message(msg,key_des)
   return decrypted_msg

def encrypt_message(msg):
   key_des=set_des_key()
   encrypted_msg=des.des_encrypt_message(msg, key_des)
   return encrypted_msg

#Sha1 (for msg validation and password storing) ------------------------------------------------------------------------------------------------------------------- 

def hash_data(Plain_Text):
    hashed_data = sha1.calculate_sha1(Plain_Text)
    return hashed_data

#RSA (for msgs sent over sockets) ------------------------------------------------------------------------------------------------------------------- 

def RSA_encrypt(plaintext,My_username):
   reciever=get_other_Username(My_username)
   public_key=get_Public_key(reciever)
   encrypted_msg=rsa.encrypt(public_key, plaintext)
   return encrypted_msg


def RSA_decrypt(cipher_text,My_username):
   Private_key=get_Private_key(My_username)
   decrypted_msg=rsa.decrypt(Private_key, cipher_text)
   return decrypted_msg