from utils.config import DASHA_NAME, DASHA_ID, IGOR_NAME, IGOR_ID


def check_user(name: str, user_id: int):
    if (name == DASHA_NAME and user_id == DASHA_ID) or (name == IGOR_NAME and user_id == IGOR_ID):
        return True
    return False


def check_developer(name: str, user_id: int):
    if name == IGOR_NAME and user_id == IGOR_ID:
        return True
    return False
