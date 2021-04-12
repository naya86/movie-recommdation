from flask import Flask
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from mysql.connector import Error
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db.db import get_mysql_connection
# 패스워드
from utils import check_password, hash_password
# 이메일 밸리데이션
from email_validator import validate_email, EmailNotValidError
# 로그아웃 기능
from flask_jwt_extended import get_jti


jwt_blocklist = set()



class UserResource(Resource) :
    def post(self) :
        
        # 바디에서 데이터 받기

        data = request.get_json()

        # 다 들어왔는지 확인 (email,password,name,gender)

        if 'eamil' not in data or 'password' not in data or 'name' not in data
            or 'gender' not in data :
            
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

            param = (data['email'], data['password'], data['name'], data['gender'])

            cursor.execute(query, param)

            cursor.commit()

            user_id = cursor.lastrowid
            print(user_id)

        except Error as e:
            return {'err_code' : 4}, HTTPStatus.METHOD_NOT_ALLOWED


        cursor.close()
        connection.close()

        # 토큰 발행

        access_token = create_access_token(identity=user_id)

        return {"token" : access_token}, HTTPStatus.OK



        
             
        

