from functools import wraps
from flask_login import current_user
from flask import abort


def roles_required(*roles: str):
    def decorator(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            if current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_func
    return decorator
