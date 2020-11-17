# from flask_sqlalchemy import SQLAlchemy
from .db_routing.routing_sqlalchemy import RoutingSQLAlchemy

from models.news import Channel

db = RoutingSQLAlchemy()
