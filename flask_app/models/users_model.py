from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, EMAIL_REGEX
from flask import flash
import re

class User:
    def __init__( self, data ):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_list = []

    @classmethod
    def create_one( cls, data ):
        query  = "INSERT INTO users( email, password, first_name, last_name ) "
        query += "VALUES( %(email)s, %(password)s, %(first_name)s, %(last_name)s ); "

        result = connectToMySQL( DATABASE ).query_db( query, data )
        return result
    
    @classmethod
    def get_one( cls, data ):
        query  = "SELECT * "
        query += "FROM users "
        query += "WHERE email = %(email)s; "

        result = connectToMySQL( DATABASE ).query_db( query, data )
        if len( result ) > 0:
            return cls( result[0] )
        else:
            flash( "Wrong credentials!", "password_login_error" )
            return None
        
    @classmethod
    def check_email(cls, data):
        query  = "SELECT * "
        query += "FROM users "
        query += "WHERE email = %(email)s; "

        result = connectToMySQL( DATABASE ).query_db( query, data )
        return result

    @staticmethod
    def validate_registration( data ):
        is_valid = True
        if len( data['first_name']) < 2 or not data['first_name'].isalpha():
            flash( "You first name is invaild, it must contain two or more charcaters and no numbers!", "first_name_error" )
            is_valid = False
        if len( data['last_name']) < 2 or not data['last_name'].isalpha():
            flash( "You last name is invaild, it must contain two or more charcaters and no numbers!", "last_name_error" )
            is_valid = False
        if data['password'] != data['password_confirmation']:
            flash( "Passwords must match!", "password_error" )
            is_valid = False
        if len( data['password']) < 8:
            flash("Password must be at least eight or more characters!", "password_error")
        if EMAIL_REGEX.match( data['email'] ): 
            current_user= {
                "email": data['email']
            }
            results = User.check_email(current_user)
            if len(results) != 0:
                flash("email is already taken!", "email_error")
                is_valid = False
        else:
            flash("Invalid email address!", "email_error")
            is_valid = False
        return is_valid

    @staticmethod
    def encrypt_password( pwd, bcrypt ):
        return bcrypt.generate_password_hash( pwd )
    
    @staticmethod
    def validate_password( pwd, encr_pwd, bcrypt ):
        if not bcrypt.check_password_hash( encr_pwd, pwd ):
            flash( "Wrong credentials!", "password_login_error" )
            return False
        else:
            return True
        