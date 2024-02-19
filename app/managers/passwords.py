from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordManager:
    def __init__(self, context: CryptContext):
        self.context = context

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.context.verify(plain_password, hashed_password)

    def get_password_hash(self, plain_password: str) -> str:
        return self.context.hash(plain_password)


password_manager = PasswordManager(pwd_context)
