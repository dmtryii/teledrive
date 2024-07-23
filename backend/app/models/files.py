
from sqlalchemy_serializer import SerializerMixin

from app.extensions import db


class File(db.Model, SerializerMixin):
    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    telegram_file_id = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('base_user.id'), nullable=False)
    