from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate

from models import db

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///demo.db"

migrate = Migrate(app=app, db=db)

db.init_app(app=app)

if __name__ == '__main__':
    app.run(debug=True)