from flaskblog import db, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
import psycopg2

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    contacts = db.relationship('Contact', backref='owner', lazy=True)


    def generate_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id' : self.id})


    @staticmethod
    def check_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None

        return User.query.get(user_id)



class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(60), nullable=False)
    number = db.Column(db.BigInteger, nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

