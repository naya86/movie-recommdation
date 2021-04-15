from flask import Flask
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from mysql.connector import Error
from db.db import get_mysql_connection


# # 영화 검색 API

# class MovieSerch(Resource) :
#     # 검색하는 영화명을 받아야하니까 post? 
#     def post(self) :
    
#     # 바디에서 데이터 가져오기. 
#         data = request.get_json()
#         #print(data)

#         if "title" not in data :
#             return {"message" : "No title has been entered."}.HTTPStatus.BAD_REQUEST
        
#         connection = get_mysql_connection()

#         cursor = connection.cursor(dictionary=True)

#         query = """ select title, count(*) as reviews_counts, 
#                     round(avg(rating),1) as average_rating 
#                     from movie as m
#                     join rating as r
#                         on m.id = r.item_id
#                     group by title 
#                     having title like %s; """
        
#         param = ('%'+ data['title'] + '%',)
#         cursor.execute( query, param)
#         records = cursor.fetchall()
#         print(records)

#         if len(records) == 0 :
#             return {"message" : "There is no movie."},HTTPStatus.NO_CONTENT

#         else :
#             return {"count" : len(records), "ret" : records}
        





        

    


