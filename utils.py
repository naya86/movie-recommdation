from passlib.hash import pbkdf2_sha256
from config.config import salt

# 회원가입시 패스워드 암호화

def hash_password(password) :
    return pbkdf2_sha256.hash(password + salt)



# 로그인시 체크

def check_password(password, hashed) :
    return pbkdf2_sha256.verify(password + salt, hashed)

    