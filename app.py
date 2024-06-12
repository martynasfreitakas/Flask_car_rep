import os
from flask import Flask
from config import Config
from routes import all_my_routes
from dotenv import load_dotenv
from database import db

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)

with app.app_context():
    all_my_routes(app)
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False,  host="0.0.0.0")
