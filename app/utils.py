from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"])



def hass_pass(password: str):
    return pwd_context.hash(password)


def verify_pass(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)