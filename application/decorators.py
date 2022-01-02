from functools import wraps
from flask_login import current_user
from flask import abort, redirect, url_for


def superuser_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if not current_user.is_superuser():
            abort(403)
        return f(*args, **kwargs)
    return decorated_func



def check_authentication(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_func
