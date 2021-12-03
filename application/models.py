from application import db, login_manager, bcrypt
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


post_tags = db.Table('post_tags',
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                     )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True, nullable=False)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    about = db.Column(db.String(256), nullable=True)
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(32), nullable=True)

    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic', passive_deletes=True,
                            cascade='all, delete, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic', passive_deletes=True,
                               cascade='all, delete, delete-orphan')

    @property
    def password(self):
        raise AttributeError('Password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def set_role(self, new_role: str):
        self.role = new_role  # Use user.set_role(None) to delete role

    def get_reset_token(self, expires_sec=300):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def is_admin(self):
        return self.role == 'admin'

    def can_create_posts(self):
        return self.role in ('admin', 'writer')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.member_since}', '{self.role}')"

    def __str__(self):
        return f'{self.username}, {self.email}, {self.role}'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic', passive_deletes=True,
                               cascade='all, delete, delete-orphan')
    tags = db.relationship('Tag', secondary=post_tags, backref='posts')

    def __repr__(self):
        return f"Post('{self.title}', '{self.content}', '{self.timestamp}')"

    def __str__(self):
        return f'{self.title}, {self.timestamp}'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"Comment('{self.post_id}', '{self.user_id}', '{self.timestamp}')"

    def __str__(self):
        return f'{self.content}, {self.timestamp}'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    # Relationships
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f"Tag('{self.name}')"

    def __str__(self):
        return f'{self.name}'
