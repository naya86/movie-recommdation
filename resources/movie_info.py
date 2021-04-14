from flask import Flask
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from mysql.connector import Error
from db.db import get_mysql_connection
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd
import numpy as np

#영화 정보
class MovieList(Resource) :
    def get(self):
        
        #쿼리스트링 가져오기
        data = request.args()   
        print(data)
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



##  영화 추천 API

class Movie_recom(Resource) :
    
    @jwt_required()
    def get(self) :
        # 이 유저가 본 영화정보 필요, 유저가 쓴 리뷰 정보 불러올 필요 있음

        user_id = get_jwt_identity() # 유저의 아이디 정보 .

        # 해당 유저가 쓴 리뷰 불러오기.

        connection = get_mysql_connection()

        cursor = connection.cursor(dictionary=True)

        query = """ select title as 'Movie Name', rating as Ratings
                    from movie as m
                    join rating as r
                        on m.id = r.item_id
                    where r.user_id = %s; """
        
        param = ( user_id, )
        
        cursor.execute(query, param)
        myRatings = cursor.fetchall()
        print(myRatings)

        cursor.close()
        connection.close()

        if len(myRatings) == 0 :
            return {"message" : "No reviews data"}

        # 영화 상관관계 csv 파일 불러오기
        movie_correlations = pd.read_csv('movie_correlations.csv', index_col=0)
        
        # 상관 관계 데이터프레임에 내 리뷰작성 정보 대입
        
        similar_movies_list = pd.DataFrame()
             
        for i in np.arange(0, len(myRatings)) :
            movie_title = myRatings[i]['Movie Name']
            similar_movie = movie_correlations[ movie_title].dropna().sort_values(ascending = False).to_frame()  
            similar_movie.columns = ['Correlation']
            similar_movie['Weight'] = similar_movie['Correlation'] * myRatings[i]['Ratings']
            similar_movies_list =  similar_movies_list.append(similar_movie)
        
        # 내가 별점 준 영화는 빼자.
        similar_movies_list = similar_movies_list.reset_index()
        
        # print(similar_movies_list.loc[similar_movies_list['title'] != myRatings[1]['Movie Name'], ])
        for i in np.arange(0, len(myRatings)) :
            similar_movies_list = similar_movies_list.loc[similar_movies_list['title'] != myRatings[i]['Movie Name'], ]

        #print(similar_movies_list)


        # 확인결과 영화명이 같은 데이터가 나올 수 있음. 그 중 weight높은 값으로 하나만 남기기.
        final_recom = similar_movies_list.groupby('title')['Weight'].max().sort_values(ascending=False).reset_index()

        final_recom['Weight'] = round(final_recom['Weight'],1)
        final_recom = final_recom.head(10).to_dict('records')
        
        print(final_recom)
        
        return {"count" : len(final_recom), "ret" : final_recom}
        




                








        








   

           

        


        