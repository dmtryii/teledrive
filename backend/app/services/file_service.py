
from typing import List
from werkzeug.datastructures.file_storage import FileStorage

from app.exceptions.auth_exception import UnauthorizedError
from app.exceptions.file_exception import FileNotFoundException, DeletionError
from app.exceptions.telegram_exception import TelegramFileNotFoundError
from app.models.files import File
from app.extensions import db
from app.services import telegram_service


def upload_files(files: List[FileStorage], user_id: int) -> List[str]:
    uploaded_files = []

    for file in files:
        if file.filename == '':
            continue

        # Step 1: Send the document
        telegram_response = telegram_service.send_document(file, user_id)
        message_id = telegram_response['result']['message_id']

        # Step 2: Delete the message
        telegram_service.delete_message(user_id, message_id)

        # Store file information in the database
        telegram_document = telegram_response['result']['document']
        store_file_info(user_id, telegram_document)

        uploaded_files.append(file.filename)

    return uploaded_files


def download_file(file_id: int, user_id: int) -> str:
    file = File.query.get(file_id)
    if not file:
        raise FileNotFoundException("File not found")

    if file.user_id != user_id:
        raise UnauthorizedError("Unauthorized to access this file")

    telegram_file_id = file.document_info.get('file_id')
    if not telegram_file_id:
        raise TelegramFileNotFoundError("Telegram file ID not found")

    file_path = telegram_service.get_file_path(telegram_file_id)
    return telegram_service.generate_file_url(file_path)


def delete_file(file_id: int, user_id: int) -> None:
    file = File.query.get(file_id)
    if not file:
        raise TelegramFileNotFoundError("File not found")

    if file.user_id != user_id:
        raise UnauthorizedError("Unauthorized to delete this file")

    try:
        db.session.delete(file)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise DeletionError(f"Error deleting file: {str(e)}")


def get_files(user_id: int) -> List[File]:
    return File.query.filter_by(user_id=user_id).all()


def store_file_info(user_id, document_info) -> None:
    new_file = File(user_id=user_id, document_info=document_info)
    db.session.add(new_file)
    db.session.commit()
