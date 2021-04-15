from flask import Flask
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from mysql.connector import Error
from db.db import get_mysql_connection
from flask_jwt_extended import get_jwt_identity, jwt_required



# 즐겨찾기 추가 API
class Favorite(Resource) :
    # 즐겨찾기 로그인 필요.
    # 데이터를 추가해야해서 post
    
    @jwt_required()
    def post(self,movie_id) : 

        # 즐겨찾기 기능은 한 영화당, 한 유저만 가능하도록 함.
        # 그럴려면 이미 있는 즐겨찾기 테이블 데이터 필요, 불러오기
        # 유저 아이디 먼저 확인
        user_id = get_jwt_identity()

        # 디비 연결 , 즐겨찾기 테이블 정보 확인 
        connection = get_mysql_connection()

        cursor = connection.cursor(dictionary=True)

        query = """ select * from favorite
                    where item_id=%s and user_id = %s; """

        param = ( movie_id, user_id )

        cursor.execute( query, param )
        records = cursor.fetchall()
        # print(records)

        # 이미 해당 영화에 이미 내 즐겨찾기에 있을 경우 ( 데이터가 이미 있음. )
        if len(records) != 0 :
            return {"message" : "Movie saved already"},HTTPStatus.BAD_REQUEST

        
        # 없을 경우 저장.
        else : 

            query = ''' insert into favorite(item_id,user_id)
                        values(%s, %s) '''
            param = ( movie_id, user_id )

            cursor.execute(query, param)
            connection.commit()

            cursor.close()
            connection.close()

            return {"message" : "Added favorite"},HTTPStatus.OK


# 즐겨찾기 삭제 API
# 삭제도 내 즐겨찾기만 삭제하므로, 로그인
    
    @jwt_required()
    def delete(self, movie_id) :

        # 디비 정보 가져오기

        user_id = get_jwt_identity()

        connection = get_mysql_connection()
        cursor = connection.cursor(dictionary=True)

        query = ''' select item_id, user_id from favorite
                    where item_id=%s and user_id=%s ; '''  

        param=(movie_id,user_id ) 

        cursor.execute(query, param)
        records = cursor.fetchall()
        #print(records)
        
        # 즐겨찾기에 없으면 삭제할 데이터가 없음.
        if len(records) == 0 :
            return {"message": 'There are no favorites to delete.'},HTTPStatus.BAD_REQUEST
        
        # 내가 저장한 즐겨찾기 맞는지 다시 확인.
        favorite_user_id = records[0]['user_id']
        # print(favorite_user_id)

        if user_id != favorite_user_id :
            return {"message" : "different user"},HTTPStatus.METHOD_NOT_ALLOWED

        # 맞으면 삭제
        query = """ delete from favorite
                    where item_id=%s and user_id = %s; """

        param=(movie_id,user_id ) 

        cursor.execute(query, param)
        connection.commit()

        cursor.close()
        connection.close()

        return {"message" : "Delete OK!"},HTTPStatus.OK

        
# 내 즐겨찾기 가져오는 API
# 로그인 필요
# 페이지 제한으로 리미트 필요 ( 쿼리 파라미터)
class MyFavorite(Resource):
    @jwt_required()
    def get(self) :        #쿼리파라미터 (offset, limit)
        # 쿼리 가져오기
        data = request.args.to_dict()
        #print(data)
        offset = int(data['offset'])
        limit = int(data['limit'])
        
        # 내 즐겨찾기 데이터 필요
        user_id = get_jwt_identity()

        connection = get_mysql_connection()
        cursor = connection.cursor(dictionary=True)

        query = """ select title, u.email 
                    from movie as m
                    join favorite as f
                        on m.id = f.item_id
                    join user as u
                        on f.user_id = u.id
                    where f.user_id = %s limit %s, %s; """

        param = (user_id,offset, limit)
        
        cursor.execute(query, param)
        records = cursor.fetchall()
        print(records)

        # records값이 없으면 즐겨찾기 해놓은 것이 없다.
        if len(records) == 0 :
            return {"message" :'There are no favorites'},HTTPStatus.BAD_REQUEST

        # 값이 있으면 출력.
        else :
            return {"count" : len(records), "favorite" : records},HTTPStatus.OK




        


        

        


            


        
