from flask import Flask, Blueprint, redirect, render_template, request, session, flash, url_for, jsonify
from pymongo import MongoClient
import re
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from dbpkg import userDB, loggedDB


bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route('/sign_up', methods=('GET', 'POST'))
def sign_up():
    if request.method == 'POST':
        email = request.form['email'] 
        name = request.form['name']
        password = request.form['password']

        if email == "" or name == "" or password == "":
            null_msg = "모든 항목을 입력해주세요."
            flash(null_msg)
        elif re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$").match(email) == None:
            error_msg = "이메일 주소가 올바르지 않습니다"
            flash(error_msg)
        elif userDB.find({"email": email}) != None:
            error_msg = "이미 가입된 이메일 주소입니다."
            flash(error_msg)
        else:
            userDB.insert({"email": email,
                        "name": name,
                        "password": generate_password_hash(password)})
            return redirect(url_for('sign_in'))
    return render_template("user/sign_up.html")
        
@bp.route('/sign_in', methods=('GET', 'POST'))
def sign_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = userDB.find({"email": email})
        if user == None:
            error_msg = "등록된 정보가 없습니다. 회원가입을 해주세요."
            render_template("user/to_sign_up.html", msg = error_msg)
        elif not check_password_hash(userDB.find_one({"email": email},{"password": 1})['password'], password):
            error_msg = "비밀번호가 틀렸습니다."
            flash(error_msg)
        else:
            session.clear()
            session['user_id'] = user
            return redirect(url_for('board'))
    return render_template("user/sign_in.html")

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id != None:
        loggedDB.insert({"logged_id": user_id})

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user_id = session.get('user_id')
        if loggedDB.find({"logged_id": user_id}) == None:
            return redirect(url_for('user.sign_in'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/sign_out')
def logout():
    user_id = session.get('user_id')
    session.clear()
    loggedDB.remove({"logged_id": user_id})
    return redirect(url_for('index'))

