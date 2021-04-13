from flask import Flask
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from mysql.connector import Error
from db.db import get_mysql_connection


class MovieList(Resource) :
    def get(self,select,page_num):

        connection = get_mysql_connection()

        cursor = connection.cursor(dictionary=True)

        # 1이면 리뷰 수 내림차순
        if select == 1 :
        
            query = """ select title,  count(user_id) as reviews_counts, round(avg(rating),1) as average_rating 
                        from movie as m
                        left join rating as r
                            on m.id = r.item_id 
                        group by m.title
                        order by reviews_counts desc limit %s, 25;  """

        #     param = ( (page_num - 1)*25 , )

        #     cursor.execute( query, param )
        #     records = cursor.fetchall()
        #     print(records)

        #     cursor.close()
        #     connection.close()
                       
        # return {"count" : len(records),"ret" : records}
            
        
        # 2면 별점 평균 내림차순
        elif select == 2 :
            query = """ select title,  count(user_id) as reviews_counts, round(avg(rating),1) as average_rating 
                        from movie as m
                        left join rating as r
                            on m.id = r.item_id 
                        group by m.title
                        order by average_rating desc limit %s, 25;  """

        param = ( (page_num - 1)*25 , )

        cursor.execute( query, param )
        records = cursor.fetchall()
        print(records)

        cursor.close()
        connection.close()
        
        return {"count" : len(records),"ret" : records} 





   

           

        


        