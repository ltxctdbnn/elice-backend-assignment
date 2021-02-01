import os
from flask import Flask, render_template, jsonify

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = "jungwoo"
    
    if test_config == None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template("index.html")

    import userpkg
    app.register_blueprint(userpkg.bp)

    return app

create_app()