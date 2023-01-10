from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = "ohana_rideshare"

class Users:
        def __init__(self,data):
                self.id = data['id']
                self.first_name = data['first_name']
                self.last_name = data['last_name']
                self.email = data['email']
                self.password = data[ "password" ]
                self.created_at = data["created_at"]
                self.updated_at = data["updated_at"]

        @classmethod
        def get_all(cls):
                query = "SELECT * FROM users;"

                results = connectToMySQL(db).query_db(query)

                users = []
                for user in results:
                        users.append(cls(user))
                return users

        @classmethod
        def save(cls,data):
                query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s,now(), now());"
                return connectToMySQL(db).query_db( query, data )
        
        @classmethod
        def get_one(cls,data):
                query  = "SELECT * FROM users WHERE id = %(id)s;"
                result = connectToMySQL(db).query_db(query,data)
                return cls(result[0])

        @classmethod
        def delete(cls,data):
                query = "delete from users where id =%(id)s;"
                return connectToMySQL(db).query_db(query,data)


        @classmethod
        def get_by_email(cls, data):
                query="SELECT * FROM users WHERE email = %(email)s;"
                results = connectToMySQL(db).query_db(query, data)
                if len(results) < 1:
                        return False
                return cls(results[0])

        @staticmethod
        def validate_register(user):
                is_valid = True
                
                query = "SELECT * FROM users WHERE email = %(email)s;"
                result = connectToMySQL(db).query_db(query,user)
                
                if len(result) >= 1:
                        is_valid = False
                        flash("User email already exist","register")
                if len(user[ 'first_name' ]) < 2:
                        flash( "Must have letters only, and at least 2 characters." ,"register")
                        is_valid = False
                if len(user[ 'last_name' ]) < 2:
                        is_valid = False
                        flash("Must have letters only, and at least 2 characters.","register")
                if len(user[ 'email' ]) <= 0:
                        flash( "Email is required." ,"register")
                        is_valid = False
                if len(user[ 'email' ]) > 0 and not EMAIL_REGEX.match(user[ 'email' ]):
                        flash("invalid email format","register")
                if len(user['password']) < 8:
                        is_valid = False
                        flash("PW must have at least 8 characters.","register")
                if user['password-confirm'] != user['password']:
                        is_valid = False
                        flash("PW must match","register")
                if not any(char.isdigit() for char in user[ 'password' ]):
                        is_valid = False
                        flash( "Password must contain at least 1 number.","register" )
                if not any(char.isupper() for char in user[ 'password' ]):
                        is_valid = False
                        flash( "Password must contain at least 1 capital letter." ,"register")
                return is_valid


