from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.users_model import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt( app )

@app.route( '/welcome', methods=['GET'] )
def get_home():
    return render_template( "home.html")

@app.route("/welcome")
def show_user():
    if 'user_id' not in session:
        return redirect("/")
    one_user = User.get_one(session['user_id'])
    return render_template("home.html", one_user = one_user)

@app.route( '/', methods=['GET'] )
@app.route( '/registration', methods=['GET'])
def get_login_registration():
    return render_template( "login_reg.html" )

@app.route( '/user/new', methods=["POST"] )
def create_user():
    if User.validate_registration( request.form ) == True:
        encrypted_password = User.encrypt_password( request.form['password'], bcrypt )
        new_user = {
            **request.form,
            "password" : encrypted_password
        }
        print(new_user)
        user_id = User.create_one( new_user )
        session[ 'full_name' ] = f"{request.form['first_name']} {request.form['last_name']}" 
        session[ 'user_id' ] = user_id
        return redirect( "/welcome" )
    else:
        return redirect( "/" ) 

@app.route( '/login', methods=['POST'] )
def user_login():
    login_user = {
        "email" : request.form["email_login"]
    }
    current_user = User.get_one( login_user )
    # current_user = User( login_user )
    if current_user != None:
        if User.validate_password( request.form["password_login"], current_user.password, bcrypt ) == True:
            session[ 'full_name' ] = f"{current_user.first_name} {current_user.last_name}" 
            session[ 'user_id' ] = current_user.id
            return redirect( "/welcome" )
        else:
            return redirect( "/" )
    else:
        flash("email does not exist", "email_login_error")
        return redirect( "/" )
    
@app.route('/logout', methods=['POST'])
def user_logout():
    session.clear()
    return redirect("/")