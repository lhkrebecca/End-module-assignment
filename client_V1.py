import socket
import pickle
from cryptography.fernet import Fernet

def send_dictionary(s):
    data = {'key': 'value', 'number': 42}
    serialized_data = pickle.dumps(data)
    s.sendall(b'dict')  
    s.sendall(serialized_data)

def send_text_file(s, file_path):
    with open(file_path, 'r') as file:
        text_data = file.read()
    s.sendall(b'text')  
    s.sendall(text_data.encode('utf-8'))

s = socket.socket()
port = 44556
s.connect(('127.0.0.1', port))

send_dictionary(s)

file_path = 'sample_text.txt'
with open(file_path, 'w') as file:
    file.write('This is a sample text file.')

# Generate a random encryption key
def generate_key():
    return Fernet.generate_key()

# Encrypt the contents of a file using the provided key
def encrypt_file(filename, key):
    cipher_suite = Fernet(key)  # Initialize a Fernet object with the encryption key
    with open(filename, 'rb') as file:
        sample_text = file.read()  # Read the sample_text data from the file
    encrypted_data = cipher_suite.encrypt(sample_text)  # Encrypt the sampe_text data
    with open(filename + '.encrypted', 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)  # Write the encrypted data to a new file

# Generate an encryption key
key = generate_key()

# Specify the source file to be encrypted
source_file = 'sample_text.txt'

# Encrypt the file using the generated key
encrypt_file(source_file, key)

# Prompt user for input
file_path = input("Enter the path to the file: ")
encrypt_option = input("Encrypt the file? (Y/N): ")

if encrypt_option.upper() == "Y":
    encrypt_file(file_path, key)
    print("File encrypted successfully.")
else:
    # Skipping encryption entirely
    with open(file_path, "r") as file:
        file_content = file.read()
    print("No encryption performed.")
    key = None  # Set `key` to `None` to indicate that no encryption was performed

# Print the encrypted content in hexadecimal format if encryption was performed
if key is not None:
    encrypted_filename = source_file + '.encrypted'
    with open(encrypted_filename, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
        encrypted = encrypted_data.hex()
        print("Encrypted Content:", encrypted)


s.close()
s = socket.socket()
s.connect(('127.0.0.1', port))

send_text_file(s, file_path)

s.close()
