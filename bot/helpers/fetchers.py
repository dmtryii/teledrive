
import requests
import config


def get_user_status(chat_id: int) -> bool:
    try:
        response = requests.get(f'{config.USER_API_URL}/{chat_id}')
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error checking user status: {e}")


def signup_user(user_data: dict) -> requests.Response:
    try:
        response = requests.post(f'{config.AUTH_API_URL}/signup', json=user_data)
        return response
    except requests.RequestException as e:
        print(f"Error signing up user: {e}")


def change_password(user_id: int, current_password: str, new_password: str) -> requests.Response:
    try:
        response = requests.patch(
            f'{config.USER_API_URL}/change_password',
            json={'user_id': user_id, 'current_password': current_password, 'new_password': new_password}
        )
        return response
    except requests.RequestException as e:
        print(f"Error changing password: {e}")
