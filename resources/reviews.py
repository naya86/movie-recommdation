from flask import Flask
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from mysql.connector import Error
from db.db import get_mysql_connection
from flask_jwt_extended import get_jwt_identity, jwt_required




class ReviewList(Resource) :
    def get(self) : # 쿼리파마미터 (movie_id, offset, limit)
        
        # 쿼리파라미터 값 가져오기
        data = request.args.to_dict()
        #print(data)
        movie_id = int(data['movie_id'])
        offset = int(data['offset'])
        limit = int(data['limit'])
        
        
        # 디비에서 데이터 가져오기
        connection = get_mysql_connection()
        cursor = connection.cursor()

        query = """ select u.name, u.gender, r.rating 
                    from movie as m
                    left join rating as r
	                   on m.id = r.item_id
                    left join user as u
	                   on u.id = r.user_id
                    where m.id = %s limit %s,%s ; """

        param = ( movie_id, offset, limit )
        
        cursor.execute(query, param)
        records = cursor.fetchall()
        # print( records )

        cursor.close()
        connection.close()
        
        return {"count" : len(records),"ret" : records}    


    # 새로운 리뷰 만들기 API
    # 리뷰는 로그인 필요
    
    
    
class NewReview(Resource) :  
    @jwt_required()  
    def post(self) :

        # 바디데이터 받기 ( 영화 아이디값 , 별점 )
        data = request.get_json()

        # 데이터 체크
        if "item_id" not in data or "rating" not in data :
            return {"message" : "No data has been entered."}.HTTPStatus.BAD_REQUEST

        # 유저 확인 위해 유저아이디 값 가져오기. (토큰)

        user_id = get_jwt_identity() # 토큰 저장.

        # 디비 연결

        connection = get_mysql_connection()
        cursor = connection.cursor()

        query = """ insert into rating (item_id, rating, user_id)
                    values (%s,%s,%s); """

        param = (data['item_id'], data['rating'], user_id)

        cursor.execute( query, param)
        
        connection.commit()

        cursor.close()
        connection.close()

        return {"message" : "Complited a new review."},HTTPStatus.OK






