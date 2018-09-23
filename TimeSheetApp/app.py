from flask import Flask
from flaskext.mysql import MySQL
from TimeSheetApp.views.index import bp as index_bp
from TimeSheetApp.config.config import secret_key as sk

app = Flask(__name__)
app.register_blueprint(index_bp)
app.secret_key = sk
