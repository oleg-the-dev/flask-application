from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app, abort
from flask_login import login_required, current_user
from application.posts.forms import PostForm, CommentForm, DeleteForm
from application.models import Post, Comment, Tag
from application import db
from application.decorators import superuser_required

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create_post', methods=['GET', 'POST'])
@login_required
@superuser_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Post has been successfully created.', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', form=form, title='Create Post')


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    delete_form = DeleteForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            post=post,
            author=current_user
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.', 'success')
        return redirect(request.url)
    page = request.args.get('page', 1, type=int)
    comments = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page=page, per_page=current_app.config['COMMENTS_PER_PAGE']
    )
    return render_template('post.html', post=post, form=form, comments=comments,
                           delete_form=delete_form)


@posts.route('/post/<int:post_id>/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(post_id, comment_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id == current_user.id or current_user.is_superuser():
        db.session.delete(comment)
        db.session.commit()
        flash('Comment has been deleted.', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    abort(403)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
@superuser_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post has been updated.', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', form=form, title='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
@superuser_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    post_title = post.title
    db.session.delete(post)
    db.session.commit()
    flash(f'«{post_title}» has been deleted', 'success')
    return redirect(url_for('main.home'))


@posts.route('/tag/<tag_name>')
def tag(tag_name):
    delete_form = DeleteForm()
    page = request.args.get('page', 1, type=int)
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    tags = Tag.query.order_by(Tag.name)
    posts = Post.query.filter(Post.tags.any(name=tag_name)).paginate(page=page,
                                                                per_page=current_app.config['POSTS_PER_PAGE'])
    return render_template('tag.html', tag=tag, tags=tags, posts=posts, delete_form=delete_form)
