from passlib.hash import pbkdf2_sha256
from config.config import salt

# 회원가입시 사용할 함수로서, 유저가 입력한 비밀번호를 암호화 해주는 함수
def hash_password(password) :
    return pbkdf2_sha256.hash(password + salt)


# 로그인시 사용할 함수
# 유저가 입력한 비밀번호와 디비에 저장된 비밀번호가 같은지 확인해 주는 함수
def check_password(password, hashed) :
    return pbkdf2_sha256.verify(password + salt, hashed)
