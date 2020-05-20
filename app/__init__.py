from flask import Flask
from app import db
from app import robots
app = Flask(__name__ , static_url_path='/static', static_folder='static')

app.config['SECRET_KEY'] = 'c07fc84ea77edced0582cbb80095795d'

db.BuildTables() # First Step Check exists and build Tables Database

# This is For test robto
# TODO: __init__ file for robot
"""
arzdigital = robots.news_from_arzdigital()
tasnim = robots.news_from_tasnimnews()
tejarat = robots.news_from_tejaratnews()
"""

from app import routes # route import 
from app.admin.routes import admin # admin route import
app.register_blueprint(admin,url_prefix='/admin') # add admin route with blueprint