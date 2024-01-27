import base64
import os
import re

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from dotenv import load_dotenv

# Loading the .env file
load_dotenv()

# Getting the keys from .env
private_key_path = os.getenv('PRIVATE_KEY_PATH')


# To get ANY user input. Keep getting input till we get a valid input
def get_user_input(input_message, validate_function):
    user_input =  input(input_message)

    try:
        validate_function(user_input)
        return user_input
    except Exception as e:
        print(e)
        return get_user_input(input_message, validate_function)

# To decrypt an encrypted password
def decrypt_password(encrypted_password):
    with open(private_key_path, "r") as key_file:
        private_key = key_file.read()
    key = RSA.importKey(private_key)
    cipher = Cipher_pkcs1_v1_5.new(key)
    decrypted_password = cipher.decrypt(base64.b64decode(encrypted_password), None)
    return decrypted_password.decode()

# To extract sharenames
def extract_sharenames(connection_output):
    pattern = r'^\s*(\w+\$?)\s+'
    share_names = re.findall(pattern, connection_output, re.MULTILINE)
    return share_names