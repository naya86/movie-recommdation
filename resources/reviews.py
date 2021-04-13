from flask import Flask
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from mysql.connector import Error
from db.db import get_mysql_connection




class ReviewList(Resource) :
    def get(self, movie_id) :
        
        # 디비에서 데이터 가져오기
        connection = get_mysql_connection()
        cursor = connection.cursor()

        query = """ select u.name, u.gender, r.rating 
                    from movie as m
                    left join rating as r
	                   on m.id = r.item_id
                    left join user as u
	                   on u.id = r.user_id
                    where m.id = %s ; """

        param = ( movie_id, )
        
        cursor.execute(query, param)
        records = cursor.fetchall()
        print( records )

