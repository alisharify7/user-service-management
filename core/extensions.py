from passlib.context import CryptContext
hashManager = CryptContext(schemes=["bcrypt"], deprecated="auto")

