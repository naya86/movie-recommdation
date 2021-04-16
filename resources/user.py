from flask import Flask
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from mysql.connector import Error
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from db.db import get_mysql_connection
# 패스워드
from utils import hash_password, check_password
# 이메일 밸리데이션
from email_validator import validate_email, EmailNotValidError
# 로그아웃 기능
from flask_jwt_extended import get_jti


jwt_blocklist = set()


## 회원가입
class UserResource(Resource) :
    def post(self) :
        
        # 바디에서 데이터 받기

        data = request.get_json()

        # 다 들어왔는지 확인 (email,password,name,gender)

        if 'email' not in data or 'password' not in data or 'name' not in data or 'gender' not in data :
            
            return {"err_code" : 1},HTTPStatus.BAD_REQUEST

        # 이메일 형식 맞는지 확인

        try :
            validate_email(data['email'])

        except EmailNotValidError as e :
            return {"err_code" : 2},HTTPStatus.NOT_FOUND   

        # 비밀 번호 길이 체크

        if len(data['password']) < 4 or len(data['password']) > 16 :
            return {"err_code" : 3}, HTTPStatus.NOT_ACCEPTABLE

        # 비밀번호 암호화
        password = hash_password( data['password'] )
        print(password)

        # 데이터베이스로 저장

        try:
            connection = get_mysql_connection()

            cursor = connection.cursor()

            query = """ insert into user(email,password,name,gender)
                    values(%s, %s, %s, %s); """

            param = (data['email'], password, data['name'], data['gender'])

            cursor.execute(query, param)

            connection.commit()

            user_id = cursor.lastrowid
            print(user_id)

        except Error as e:
            return {'err_code' : 4}, HTTPStatus.METHOD_NOT_ALLOWED


        cursor.close()
        connection.close()

        # 토큰 발행

        access_token = create_access_token(identity=user_id)

        return {"token" : access_token}, HTTPStatus.OK



## 로그인 API

class UserLogin(Resource) :
    # 로그인 API
    def post(self) :
        
        # 1. 데이터가져오기 
        data = request.get_json()

        # 2. 이메일 패스워드 있는지 확인.
        if 'email' not in data or 'password' not in data :
            return {'err_code' : 1},HTTPStatus.BAD_REQUEST

        # 3. 이메일 밸리데이션 체크
        try:
            # Validate.
            validate_email(data['email'])

            
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            print(str(e))
            return {'err_code' : 2}, HTTPStatus.NOT_FOUND
        
        
        # 4. 이메일 패스워드 맞는지 확인.
        # 디비에서 패스워드 가져오기
        
        connection = get_mysql_connection()

        cursor = connection.cursor(dictionary=True)

        query = """ select * from user
                    where email = %s;  """

        param = ( data['email'] , )

        cursor.execute(query, param)
        records = cursor.fetchall()
        print(records)

        # 4-1. 회원가입이 안된 이메일 요청시 rdcords에 데이터가 없다.
        # 클라이언트에게 응답해줘야한다.

        if len(records) == 0 :
            return {'err_code' : 3}, HTTPStatus.METHOD_NOT_ALLOWED 

        # 5. 위에서 가져온 디비에 저장되어 있는 비밀번호와 클라이언트로부터 받은 비밀번호를
        # 암호화 한것과 비교.

        password = data['password']
        hashed = records[0]['password']

        ret = check_password(password, hashed)

        # 6. 같으면 클라이언트에 리턴

        if ret is True :
            
            user_id = records[0]['id']
            access_token = create_access_token(identity=user_id)

            return {'token' : access_token},HTTPStatus.OK

        else :
            return {'err_code' : 4}, HTTPStatus.NOT_ACCEPTABLE



## 로그아웃 API 만들기

class UserLogout(Resource) :
    @jwt_required()
    def post(self) :
        
        jti = get_jwt()['jti']
        jwt_blocklist.add(jti)

        return {'message' : 'Log Out'},HTTPStatus.OK


## 내 정보 가져오기 API

class UserInformation(Resource) :
    @jwt_required()
    def get(self) :

        # 로그인한 유저 아이디 가져오기
        user_id = get_jwt_identity()

        # 데이터 정보가져오기

        connection = get_mysql_connection()

        cursor = connection.cursor(dictionary=True)

        query = """ select email, name, gender 
                    from user
                    where id = %s; """

        param = (user_id,)

        cursor.execute(query, param)
        user_info = cursor.fetchall()
        #print(user_info)

        if len(user_info) == 0 :
            return {"err_code" : 1},HTTPStatus.BAD_REQUEST

        query = """ select title, rating
                    from movie as m
                    join rating as r
                        on m.id = r.item_id
                    join user as u
                        on u.id = r.user_id
                    where u.id = %s; """

        param = (user_id,)

        cursor.execute(query,param)
        review_info = cursor.fetchall()
        #print(review_info)

        if len(review_info) == 0 :
            review_info = "No review information"
            
            # return {"message" : "No review information"}

        return {"user_info" : user_info, "review_info" : review_info},HTTPStatus.OK
        



        
        

        

                 





        
             
        

