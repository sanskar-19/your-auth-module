from cryptography.fernet import Fernet


def encode_password(user_password:str) -> bytes:

    user_password = bytes(user_password, 'utf-8')
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    ciphered_text = cipher_suite.encrypt(user_password)   #required to be bytes

    return key,ciphered_text
    

def password_matcher(key,user_db_password,user_password:bytes) -> bool: # both the user_password and user_db_password are encrypteed and then decoded to check for correct credentials
    
    cipher_suite = Fernet(key)
    unciphered_text = (cipher_suite.decrypt(user_db_password))
    user_password = bytes(user_password, 'utf-8')
    if unciphered_text == user_password:
        return True
    
    return False
    
       