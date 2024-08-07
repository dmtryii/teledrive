
from typing import List
from werkzeug.datastructures.file_storage import FileStorage

from app.exceptions.auth_exception import UnauthorizedError
from app.exceptions.file_exception import FileNotFoundException, DeletionError, FileUploadError
from app.exceptions.telegram_exception import TelegramFileNotFoundError
from app.models.files import File
from app.extensions import db
from app.services import telegram_service, folder_services


FILES_SIZE_LIMIT = 1.5 * 1024 * 1024 * 1024
SINGLE_FILE_SIZE_LIMIT = 500 * 1024 * 1024


def upload_files(files: List[FileStorage], user_id: int, folder_id: int = None) -> List[str]:
    if folder_id is None:
        folder_id = folder_services.get_root_folder(user_id).id

    uploaded_files = []
    total_size = 0

    for file in files:
        if file.filename == '':
            continue

        file_size = get_size(file)

        if file_size > SINGLE_FILE_SIZE_LIMIT:
            raise FileUploadError(f"File {file.filename} exceeds the single file size limit of 500 MB")

        total_size += file_size
        if total_size > FILES_SIZE_LIMIT:
            raise FileUploadError(f"Total size of files exceeds the maximum allowed size of 1.5 GB")

        # Step 1: Send the document
        telegram_response = telegram_service.send_document(file, user_id)
        message_id = telegram_response['result']['message_id']

        # Step 2: Delete the message
        telegram_service.delete_message(user_id, message_id)

        # Store file information in the database
        telegram_document = telegram_response['result']['document']
        store_file_info(user_id, telegram_document, folder_id)

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


def set_file_folder(user_id: int, file_id: int, folder_id: int) -> File:
    file = get_file(user_id, file_id)
    folder = folder_services.get_folder(user_id, folder_id)
    file.folder_id = folder.id

    db.session.commit()
    return file


def get_file(user_id: int, file_id: int) -> File:
    file = File.query.get(file_id)
    if not file:
        raise TelegramFileNotFoundError("File not found")

    if file.user_id != user_id:
        raise UnauthorizedError("No permission for this file")

    return file


def store_file_info(user_id: int, document_info: dict, folder_id: int = None) -> None:
    if folder_id is None:
        folder_id = folder_services.get_root_folder(user_id).id

    new_file = File(user_id=user_id, document_info=document_info, folder_id=folder_id)
    db.session.add(new_file)
    db.session.commit()


def get_size(file: FileStorage) -> int:
    file.stream.seek(0, 2)
    file_size = file.stream.tell()
    file.stream.seek(0)

    return file_size
