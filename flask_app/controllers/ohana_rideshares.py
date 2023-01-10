from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import Users
from flask_app.models.ohana_rideshare import Ohana_Rideshare


@app.route('/dashboard')
def dashboard():
        if 'user_id' not in session:
                return redirect( '/login' )
        data ={ 'id': session[ 'user_id' ]}
        return render_template('dashboard.html', user = Users.get_one(data), rides = Ohana_Rideshare.get_all(),
        all_users = Users.get_all())

@app.route( "/ride/new" )
def ride_new():
        if 'user_id' not in session:
                return redirect( '/login' )
        return render_template( "ride_new.html" )

@app.route( "/ride/request", methods=[ "post" ])
def ride_request():
        if 'user_id' not in session:
                return redirect( '/login' )
        if not Ohana_Rideshare.validate_ride(request.form):
                return redirect( "/ride/new" )

        data ={
                'destination': request.form[ "destination" ],
                'pickup_location': request.form[ "pickup_location" ],
                'rideshare_date': request.form[ "rideshare_date" ],
                'details': request.form[ "details" ],
                'user_id': session[ "user_id" ]
        }
        Ohana_Rideshare.save(data)
        return redirect( "/dashboard" )

@app.route( "/assign/driver/<int:id>" )
def add_driver(id):
        if 'user_id' not in session:
                return redirect( '/login' )
        data = {
                'id': id,
                'driver_id': session[ 'user_id' ]
        }
        Ohana_Rideshare.assign_driver(data)
        return redirect( "/dashboard" )

@app.route( "/remove/driver/<int:id>" )
def cancel(id):
        if 'user_id' not in session:
                return redirect( '/login' )
        data ={
                'id':id
        }
        Ohana_Rideshare.remove_driver(data)
        return redirect( "/dashboard" )

@app.route( "/rides/<int:id>" )
def details(id):
        if 'user_id' not in session:
                return redirect( '/login' )
        data = {
                'id':id
        }
        return render_template( "ride_details.html", rides = Ohana_Rideshare.get_one(data), all_users = Users.get_all())

@app.route( "/delete/<int:id>" )
def delete_ride(id):
        if 'user_id' not in session:
                return redirect( '/login' )
        data = {
                "id":id
        }
        Ohana_Rideshare.delete(data)
        return redirect( "/dashboard" )

@app.route( "/rides/edit/<int:id>" )
def edit_ride(id):
        if 'user_id' not in session:
                return redirect( '/login' )
        data= {
                "id":id
        }
        return render_template( "ride_edit.html", ride = Ohana_Rideshare.get_one(data))

@app.route( "/ride/update/<int:id>", methods=[ "post" ] )
def ride_update(id):
        if 'user_id' not in session:
                return redirect( '/login' )
        if not Ohana_Rideshare.validate_ride_edit(request.form):
                return redirect(f"/rides/edit/{id}" )
        data = {
                'id':id,
                "pickup_location": request.form[ "pickup_location" ],
                "details": request.form[ "details" ],
        }
        Ohana_Rideshare.update(data)
        return redirect( f"/rides/{data[ 'id' ]}" )