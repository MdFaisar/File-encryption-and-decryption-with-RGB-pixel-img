import hashlib
import pyaes

def hash_password(password, salt):
    password_hash = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    return password_hash

def verify_password(stored_password, provided_password, salt):
    password_hash = hashlib.sha512((provided_password + salt).encode('utf-8')).hexdigest()
    print("Hashed Password:", password_hash)
    print("Password Matched", password_hash == stored_password)
    return password_hash

def AES(user_password, provided_salt):
    # Hash the password
    hashed_password = hash_password(user_password, provided_salt)
    print("Hashed Password:", hashed_password)

    key = "THE_secret_KEY_is_SECRET_becaus!"
    plaintext = hashed_password

    # key must be bytes, so we convert it
    key = key.encode('utf-8')

    aes = pyaes.AESModeOfOperationCTR(key)    
    ciphertext = aes.encrypt(plaintext)

    # show the encrypted data
    print(ciphertext)
    
    # decryption
    aes = pyaes.AESModeOfOperationCTR(key)

    # decrypted data is always binary, need to decode to plaintext
    decrypted = aes.decrypt(ciphertext).decode('utf-8')

    print(decrypted == plaintext)

    # Verify a password
    print("Decrypted_hash", decrypted)
    provided_password = input("Enter the password:")
    user_name = input("Enter the user name:")

    password_matched = verify_password(decrypted, provided_password, user_name)
    print("Hash Matched:", decrypted == password_matched)