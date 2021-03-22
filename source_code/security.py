from source_code.models.user_model import UserModel
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
    # find correct user
    user = UserModel.find_by_user_name(username)

    # compere password to one that we received
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_user_id(user_id)
