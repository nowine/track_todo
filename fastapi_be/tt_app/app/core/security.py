from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(
    schemes=['pbkdf2_sha256'],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)

def encrypt_password(password: str) -> str:
    return pwd_context.encrypt(password + settings.SALT)

def check_encrypted_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password + settings.SALT, hashed)