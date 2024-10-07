from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import os


# Function to encrypt email address
def handler(data, log):
    key = os.getenv("AES_KEY").encode('utf-8')

    email = data['email']

    # AES key must be either 16, 24, or 32 bytes
    cipher = AES.new(key, AES.MODE_CBC)  # CBC mode with a random IV
    iv = cipher.iv  # Get the Initialization Vector (IV)

    # Pad the email to be a multiple of 16 bytes
    padded_email = pad(email.encode(), AES.block_size)

    # Encrypt the padded email
    encrypted_email = cipher.encrypt(padded_email)

    # Return IV + encrypted email encoded in base64 (to make it easier to store or send)
    encrypted_email = base64.b64encode(iv + encrypted_email).decode()
    data['email_encrypted'] = encrypted_email
    return data
