from flask import Flask, Blueprint, redirect, render_template, request, session, flash, url_for, jsonify
from werkzeug.exceptions import abort
from userpkg import login_required
from dbpkg import userDB, loggedDB, boardDB
from pymongo import MongoClient

bp = Blueprint('board', __name__)

app.register_blueprint(board, bp)
app.add_url_rule('/')

db = boardDB

@bp.route('index/<board_name>')
def index(board_name):
    if db.find({"board_name": board_name}) == None:
        board_list = db.find({})
        result = jsonify(board_list)
        return render_template('main.html', board=result)
    else:
        board_list = db.find({"board_name": board_name})
        result = jsonify(board_list)
        return render_template('main.html', board=result)

@bp.route('/', methods=('GET', 'POST'))
def main():
    if request.method == "POST":
        board_name = request.form['board_name']
        return redirect(url_for('index/{}'.format(board_name)))
    return render_template('main.html')

@bp.rout('/create', methods=('GET', 'POST'))
def create():
    if request.method == "POST":
        board_name = request.form['board_name']
        title = request.form['title']
        content = request.form['content']
        
        error = None

        if board_name == None or title == None or content == None:
            error = "입력이 유효하지 않습니다."
        
        if error != None:
            flash(error)
        else:
            db.insert({"board_name": board_name, "title": title, "content": content})





