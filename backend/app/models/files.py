
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.dialects.postgresql import JSON

from app.extensions import db


class File(db.Model, SerializerMixin):
    __tablename__ = 'file'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('base_user.id'), nullable=False)
    document_info = db.Column(JSON, nullable=False)

    serialize_rules = (
        '-owner.files',
    )
