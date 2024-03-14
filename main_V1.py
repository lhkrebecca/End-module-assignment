import socket
import pickle
from cryptography.fernet import Fernet

# Generate a random encryption key
def generate_key():
    return Fernet.generate_key()

# Encrypt the contents of a file using the provided key
def encrypt_file(filename, key):
    cipher_suite = Fernet(key)  # Initialize a Fernet object with the key
    with open(filename, 'rb') as file:
        sample_text = file.read()  # Read the sample_text data from the file
    encrypted_data = cipher_suite.encrypt(sample_text)  # Encrypt the sample_text
    with open(filename + '.encrypted', 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)  # Write the encrypted data to a new file

# Decrypt the contents of an encrypted file using the provided key
def decrypt_file(encrypted_filename, key):
    cipher_suite = Fernet(key)  # Initialize a Fernet object with the key
    with open(encrypted_filename, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()  # Read the encrypted data from the file
    decrypted_data = cipher_suite.decrypt(encrypted_data)  # Decrypt the data
    decrypted_filename = encrypted_filename.replace('.encrypted', '.decrypted')  # Generate a new filename
    with open(decrypted_filename, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)  # Write the decrypted data to a new file

key = generate_key()  # Generate an encryption key
source_file = 'sample_text.txt'  # Specify the source file to be encrypted

# Encrypt the file using the generated key
encrypt_file(source_file, key)

encrypted_file = source_file + '.encrypted'  # Generate the name of the encrypted file

# Decrypt the encrypted file using the same key
decrypt_file(encrypted_file, key)

# Inform the user about the successful decryption
print(f'{encrypted_file} decrypted.')

# Print the content of the decrypted file
decrypted_filename = source_file + '.decrypted'
with open(decrypted_filename, 'r') as decrypted_file:
    decrypted_content = decrypted_file.read()
    print("Decrypted Content:\n", decrypted_content)

def process_received_data(conn):
    data_type = conn.recv(1024).decode('latin-1')
    if data_type == 'dict':
        received_data = conn.recv(1024)
        data = pickle.loads(received_data)
        print("Received dictionary:", data)
    elif data_type == 'text':
        received_text = conn.recv(1024).decode('latin-1')
        print("Received text:", received_text)
        with open('received_text.txt', 'w') as f:
            f.write(received_text)

s = socket.socket()
port = 44556
s.bind(('', port))
s.listen(5)

print("Server listening...")
while True:
    c, addr = s.accept()
    print(f"Connection from {addr} has been established.")
    process_received_data(c)
    c.close()
