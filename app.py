from flask import Flask
from flask_restful import Api
from config.config import Config
from flask_jwt_extended import JWTManager
from resources.user import UserResource, UserLogin, UserLogout, jwt_blocklist,UserInformation
from resources.movie_info import MovieList, Movie_recom
from resources.reviews import ReviewList, NewReview
from resources.serch import MovieSerch
from resources.favorite import Favorite, MyFavorite


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
api.add_resource(UserResource, '/v1/users/register')
api.add_resource(UserLogin, '/v1/users/login')
api.add_resource(UserLogout, '/v1/users/logout')
api.add_resource(MovieList, '/v1/movie')   
#MoavieList 쿼리파라미터 (offset, limit, order)
# order = reviews_counts   ,   average_rating

api.add_resource(ReviewList, '/v1/reviews')
#ReviewList 쿼리파라미터 (movie_id, offset, limit)

api.add_resource(MovieSerch, '/v1/movie/search')  
#MovieSerch 쿼리파라미터 (offset, limit, keyword)

api.add_resource(NewReview, '/v1/reviews/new')
api.add_resource(Movie_recom, '/v1/movierecommandation')
api.add_resource(UserInformation, '/v1/users/me')
api.add_resource(Favorite, '/v1/favorite/<int:movie_id>')
api.add_resource(MyFavorite, '/v1/favorite/me')



if __name__ == '__main__' :
    app.run()