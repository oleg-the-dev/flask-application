from application import create_app, db
from application.models import User, Post, Comment

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Post': Post,
        'Comment': Comment
    }


@app.before_request
def before_request():
    from flask_login import current_user
    from datetime import datetime
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


if __name__ == '__main__':
    app.run()
