
from datetime import datetime

from app.extensions import db, bcrypt


class BaseUser(db.Model):
    __tablename__ = 'base_user'

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(255), nullable=False)
    registration = db.Column(db.DateTime, default=datetime.now, nullable=False)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))

    files = db.relationship('File', backref='user_files', lazy=True)
    roles = db.relationship('Role', secondary='user_roles')
    folders = db.relationship('Folder', back_populates='user')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'registration': self.registration.isoformat(),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'files': [file.to_dict() for file in self.files],
            'roles': [role.to_dict() for role in self.roles],
            'folders': [folder.to_dict() for folder in self.folders]
        }


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.BigInteger, db.ForeignKey('base_user.id'), primary_key=True),
    db.Column('role_id', db.BigInteger, db.ForeignKey('role.id'), primary_key=True)
)
