from flask import Flask
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from mysql.connector import Error
from db.db import get_mysql_connection


# 영화 검색 API

class MovieSerch(Resource) :
    
    def get(self) : #쿼리파라미터 (offset, limit, keyword)
    
        # 쿼리에서 데이터 가져오기. 
        data = request.args.to_dict()
        #print(data)
        offset = int(data['offset'])
        limit  = int(data['limit'])
        keyword = data['keyword']
        print(offset)
        print(limit)
        print(keyword)

        # 데이터베이스에서 비교
        
        connection = get_mysql_connection()

        cursor = connection.cursor(dictionary=True)

        query = """ select title, count(*) as reviews_counts, 
                    round(avg(rating),1) as average_rating 
                    from movie as m
                    join rating as r
                        on m.id = r.item_id
                    group by title 
                    having title like %s limit %s, %s; """
        
        param = ('%'+keyword+'%', offset, limit)
        print(param)
        cursor.execute( query, param)
        records = cursor.fetchall()
        print(records)

        if records == [] : 
            return {"message" : "There is no movie."},HTTPStatus.NO_CONTENT

        # else :
        #     return {"count" : len(records), "ret" : records}
        





        

    


