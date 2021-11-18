from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from application.posts.forms import PostForm, CommentForm
from application.models import Post, Comment
from application import db
from application.decorators import roles_required

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create_post', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'writer')
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
    return render_template('post.html', post=post, form=form, comments=comments)


@posts.route('/post/<int:post_id>/delete_comment/<int:comment_id>')
@login_required
def delete_comment(post_id, comment_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment has been deleted.', 'success')
    return redirect(url_for('posts.post', post_id=post.id))


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'writer')
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


@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'writer')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    post_title = post.title
    db.session.delete(post)
    db.session.commit()
    flash(f'«{post_title}» has been deleted', 'success')
    return redirect(url_for('main.home'))
