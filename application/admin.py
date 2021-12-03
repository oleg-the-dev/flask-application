from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_login import current_user
from flask import redirect, url_for, request, abort


class AdminMixin:
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to sign in page if user doesn't have access
        if current_user.is_authenticated:
            abort(403)
        else:
            return redirect(url_for('users.sign_in', next=request.url))


class AdminHomeView(AdminMixin, AdminIndexView):
    @expose('/')
    def index(self):
        from application.models import User, Post, Comment, Tag
        context = {
            'User': User,
            'Post': Post,
            'Comment': Comment,
            'Tag': Tag,
        }
        return self.render('admin/index.html', context=context)


class AdminUserView(AdminMixin, ModelView):
    can_create = False
    column_list = ['username', 'email', 'member_since', 'last_seen', 'role']
    column_searchable_list = ['username', 'email']
    column_editable_list = ['role']
    form_excluded_columns = ['password_hash']
    form_choices = {
        'role': [
            ('admin', 'admin'),
            ('writer', 'writer')
        ]
    }


class AdminPostView(AdminMixin, ModelView):
    column_list = ['title', 'timestamp', 'author', 'tags']
    column_searchable_list = ['title']


class AdminCommentView(AdminMixin, ModelView):
    pass


class AdminTagView(AdminMixin, ModelView):
    pass
