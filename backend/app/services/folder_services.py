from typing import List

from app.exceptions.auth_exception import UnauthorizedError
from app.exceptions.folder_exception import FolderException
from app.exceptions.telegram_exception import TelegramFileNotFoundError
from app.exceptions.user_exception import EmptyFieldException
from app.models.files import Folder
from app.extensions import db


def create_folder(name: str, user_id: int, parent_id: int) -> Folder:

    if not name:
        raise EmptyFieldException(message='Missing name')

    if not parent_id:
        parent_id = get_root_folder(user_id).id

    new_folder = Folder(name=name, user_id=user_id, parent_id=parent_id)
    db.session.add(new_folder)
    db.session.commit()

    return new_folder


def get_all_folders(user_id: int) -> List[Folder]:
    return Folder.query.filter_by(user_id=user_id).all()


def get_folder(user_id: int, folder_id: int) -> Folder:
    folder = Folder.query.get(folder_id)
    if not folder:
        raise TelegramFileNotFoundError("Folder not found")

    if folder.user_id != user_id:
        raise UnauthorizedError("No permission for this folder")

    return folder


def get_root_folder(user_id: int) -> Folder:
    root_folder = Folder.query.filter_by(user_id=user_id, parent_id=None).first()
    if not root_folder:
        root_folder = Folder(name="root", user_id=user_id, parent_id=None)
        db.session.add(root_folder)
        db.session.commit()
    return root_folder


def delete_folder(user_id: int, folder_id: int) -> None:
    folder = get_folder(user_id, folder_id)

    def delete_contents(folder_delete_id: int) -> None:
        subfolders = Folder.query.filter_by(parent_id=folder_delete_id).all()
        for subfolder in subfolders:
            delete_contents(subfolder.id)
            db.session.delete(subfolder)

        files = get_folder(user_id, folder_delete_id).files
        for file in files:
            db.session.delete(file)

    delete_contents(folder_id)

    db.session.delete(folder)
    db.session.commit()


def move_folder(user_id: int, folder_id: int, destination_folder_id: int) -> Folder:
    folder = get_folder(user_id, folder_id)
    destination_folder = get_folder(user_id, destination_folder_id)

    if folder.id == destination_folder.id or is_descendant(folder, destination_folder):
        raise FolderException("Cannot move folder into itself or one of its subfolders")

    folder.parent_id = destination_folder.id
    db.session.commit()

    return folder


def get_all_available_to_move(user_id: int, folder_id: int) -> List[Folder]:
    current_folder = get_folder(user_id, folder_id)
    available_to_move = [folder for folder in get_all_folders(user_id)
                         if not is_descendant(current_folder, folder)]
    return available_to_move


def is_descendant(folder: Folder, potential_parent: Folder) -> bool:
    current = potential_parent
    while current is not None:
        if current.id == folder.id:
            return True
        current = Folder.query.get(current.parent_id)
    return False
