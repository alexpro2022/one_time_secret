from cryptography.fernet import Fernet

from src.config import app_conf

cipher_suite = Fernet(key=app_conf.secret_key.get_secret_value().encode())


def encrypt(data: str) -> str:
    return cipher_suite.encrypt(data.encode()).decode()


def decrypt(data: str) -> str:
    return cipher_suite.decrypt(data).decode()
