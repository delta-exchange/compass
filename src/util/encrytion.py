from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii
import os
from .logger import logger

class Encrpytion:
    @staticmethod
    def decrypt_kyc_data(vector, cipher):
        try:
            aes_key = os.getenv("AES_KEY")
            key, iv, ciphertext = binascii.unhexlify(aes_key), binascii.unhexlify(vector),  binascii.unhexlify(cipher)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"error while decrypting kyc data: {e}")