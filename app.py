from flask import Flask
from flask_restful import Api
from config.config import Config
from flask_jwt_extended import JWTManager
from resources.user import UserResource, UserLogin, UserLogout, jwt_blocklist
from resources.movie_info import MovieList, Movie_recom
from resources.reviews import ReviewList, NewReview
from resources.serch import MovieSerch

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
api.add_resource(UserLogout, '/v1/users/logout')
api.add_resource(MovieList, '/v1/movie/<int:select>/<int:page_num>')
api.add_resource(ReviewList, '/v1/reviews/<int:movie_id>/<int:page_num>')
api.add_resource(MovieSerch, '/v1/serch')  
api.add_resource(NewReview, '/v1/reviews/newreview')
api.add_resource(Movie_recom, '/v1/movierecommandation')

if __name__ == '__main__' :
    app.run()