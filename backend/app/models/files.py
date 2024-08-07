from datetime import datetime

from sqlalchemy.dialects.postgresql import JSON

from app.extensions import db


class Folder(db.Model):
    __tablename__ = 'folder'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('base_user.id'), nullable=False)
    parent_id = db.Column(db.BigInteger, db.ForeignKey('folder.id'))

    parent = db.relationship('Folder', remote_side=[id], backref='subfolders')
    files = db.relationship('File', backref='folder', lazy=True)
    user = db.relationship('BaseUser', back_populates='folders')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'parent_id': self.parent_id,
            'files': [file.to_dict() for file in self.files],
            'subfolders': [subfolder.to_dict() for subfolder in self.subfolders]
        }


class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.BigInteger, primary_key=True)
    upload = db.Column(db.DateTime, default=datetime.now, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('base_user.id'), nullable=False)
    folder_id = db.Column(db.BigInteger, db.ForeignKey('folder.id'))
    document_info = db.Column(JSON, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'upload': self.upload.isoformat(),
            'user_id': self.user_id,
            'folder_id': self.folder_id,
            'document_info': self.document_info
        }
