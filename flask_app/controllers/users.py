from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import Users
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route( "/" )
def index():
        return redirect( "/login" )

@app.route( "/login" )
def login():
        return render_template("index.html")

@app.route( '/register' , methods=['post'])
def form():
        if not Users.validate_register(request.form):
                return redirect( '/login' )
        
        data={
                "first_name": request.form[ 'first_name' ],
                "last_name": request.form[ 'last_name' ],
                "email": request.form[ 'email' ],
                "password": bcrypt.generate_password_hash(request.form[ 'password' ]),
        }
        
        id = Users.save(data)
        session[ 'user_id' ] = id
        print(data)
        return redirect( '/dashboard' )

@app.route('/login', methods=['post'])
def login_form():
        user = Users.get_by_email(request.form)
        
        if not request.form[ "email" ]:
                flash( "Email required.","login" )
                return redirect("/")
        if not user:
                flash("Email not found.","login")
                return redirect('/')
        if not bcrypt.check_password_hash(user.password, request.form[ 'password' ]):
                flash("Password does not match.","login")
                return redirect('/')

        session[ 'user_id' ] = user.id
        return redirect('/dashboard')

@app.route( "/logout" )
def logout():
        session.clear()
        return redirect( "/" )
