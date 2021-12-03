from flask import Blueprint, render_template, request, current_app
from application.models import Post, Tag

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page,
                                                                per_page=current_app.config['POSTS_PER_PAGE'])
    tags = Tag.query.order_by(Tag.name)
    return render_template('home.html', posts=posts, tags=tags)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/contact')
def contact():
    return render_template('contact.html')
