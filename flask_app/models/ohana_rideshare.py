from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from .user import Users

db = "ohana_rideshare"

class Ohana_Rideshare:
        def __init__(self, data):
                self.id = data[ 'id' ]
                self.destination = data[ 'destination' ]
                self.pickup_location = data[ 'pickup_location' ]
                self.rideshare_date = data[ 'rideshare_date' ]
                self.details = data[ 'details' ]
                self.created_at = data[ 'created_at' ]
                self.updated_at = data[ 'updated_at' ]
                self.driver_id = data[ 'driver_id' ]
                self.user_id = data[ 'user_id' ]
                self.users = None
        
        @classmethod
        def get_all(cls):
                query = """
                SELECT * FROM rides
                JOIN users on rides.user_id = users.id; """
                results = connectToMySQL(db).query_db(query)
                rides = []
                for row in results:
                        this_ride = cls(row)
                        user_data = {
                                'id': row[ "users.id" ],
                                'first_name': row[ "first_name" ],
                                'last_name': row[ "last_name" ],
                                'email': row[ "email" ],
                                'password': "",
                                'created_at': row[ "created_at" ],
                                'updated_at': row[ "updated_at" ]
                        }
                        this_ride.users = Users(user_data)
                        rides.append(this_ride)
                return rides

        @classmethod
        def get_one(cls,data):
                query = """
                SELECT * FROM rides 
                JOIN users on rides.user_id= users.id
                WHERE rides.id = %(id)s"""
                result = connectToMySQL(db).query_db(query,data)

                if not result:
                        return False

                result = result[0]
                this_ride = cls(result)
                user_data = {
                        'id': result[ "users.id" ],
                        'first_name': result[ "first_name" ],
                        'last_name': result[ "last_name" ],
                        'email': result[ "email" ],
                        'password': "",
                        'created_at': result[ "created_at" ],
                        'updated_at': result[ "updated_at" ]
                }
                this_ride.users = Users(user_data)
                return this_ride
                

        @classmethod
        def save(cls, data):
                query = """
                INSERT INTO rides (destination, pickup_location, rideshare_date, details,user_id)
                VALUES(%(destination)s, %(pickup_location)s, %(rideshare_date)s, %(details)s,%(user_id)s);"""
                return connectToMySQL(db).query_db(query,data)

        @classmethod
        def assign_driver(cls,data):
                query ="UPDATE rides set driver_id = %(driver_id)s WHERE id = %(id)s;"
                return connectToMySQL(db).query_db(query,data)
        
        @classmethod
        def remove_driver(cls,data):
                query ="UPDATE rides set driver_id = null WHERE id = %(id)s;"
                return connectToMySQL(db).query_db(query,data)
        
        @classmethod
        def delete(cls,data):
                query = "DELETE FROM rides WHERE id = %(id)s;"
                return connectToMySQL(db).query_db(query,data)
        
        @classmethod
        def update(cls,data):
                query ="""
                UPDATE rides set  pickup_location = %(pickup_location)s
                , details = %(details)s WHERE id = %(id)s;"""
                return connectToMySQL(db).query_db(query,data)
        
        @staticmethod
        def validate_ride(form_data):
                is_valid = True

                if len(form_data['destination']) <= 0:
                        flash("Destination is required!", "new_ride")
                        is_valid = False
                elif len(form_data['destination']) < 3:
                        flash("Name must be at least 3 characters long.", "new_ride")
                        is_valid = False
                if len(form_data['pickup_location']) <= 0:
                        flash("Pick-up Location is required!", "new_ride")
                        is_valid = False
                elif len(form_data['pickup_location']) < 3:
                        flash("Name must be at least 3 characters long.", "new_ride")
                        is_valid = False
                if form_data['rideshare_date'] == '':
                        flash("Please input a date.", "new_ride")
                        is_valid = False
                if len(form_data['details']) <= 0:
                        flash("Details is required!", "new_ride")
                        is_valid = False
                elif len(form_data['details']) < 10:
                        flash("Name must be at least 10 characters long.", "new_ride")
                        is_valid = False

                return is_valid

        @staticmethod
        def validate_ride_edit(form_data):
                is_valid = True

                if len(form_data['pickup_location']) <= 0:
                        flash("Pick-up Location is required!", "ride_edit")
                        is_valid = False
                elif len(form_data['pickup_location']) < 3:
                        flash("Name must be at least 3 characters long.", "ride_edit")
                        is_valid = False
                if len(form_data['details']) <= 0:
                        flash("Details is required!", "ride_edit")
                        is_valid = False
                elif len(form_data['details']) < 10:
                        flash("Name must be at least 10 characters long.", "ride_edit")
                        is_valid = False
                        
                return is_valid