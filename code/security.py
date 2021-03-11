from user import User
from werkzeug.security import safe_str_cmp

users = [
    User(1, 'bob', 'asdf')
]

user_name_mapping = {u.user_name: u for u in users}
user_id_mapping = {u.id: u for u in users}


def authenticate(username, password):
    # find correct user
    user = user_name_mapping.get(username, None)

    # compere password to one that we received
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return user_id_mapping.get(user_id, None)
