from flask import Flask
from flask_restful import Api
from config.config import Config
from flask_jwt_extended import JWTManager
from resources.user import UserResource, UserLogin


app = Flask(__name__)

# 콘픽 환경 설정.

app.config.from_object(Config)

# JWT 로그인 환경 설정

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) :
    jti = jwt_payload['jti']
    return jti in jwt_blocklist

# API 설정

api = Api(app)

# 경로 연결
api.add_resource(UserResource, '/v1/users')
api.add_resource(UserLogin, '/v1/users/login')




if __name__ == '__main__' :
    app.run()