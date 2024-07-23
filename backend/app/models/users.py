
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

from app.extensions import db, bcrypt


class BaseUser(db.Model, SerializerMixin):
    __tablename__ = 'base_user'

    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(255), nullable=False)    
    registration = db.Column(db.DateTime, default=datetime.now, nullable=False)

    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    
    files = db.relationship('File', backref='owner', lazy=True)
    roles = db.relationship('Role', secondary='user_roles')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    
class Role(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('base_user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)
