from flask import Blueprint, render_template, current_app, request
from werkzeug.exceptions import abort

from bp_posts.dao.comment_dao import CommentDAO
from bp_posts.dao.post_dao import PostDAO
from config import DATA_PATH_POST, DATA_PATH_COMMENTS

# Создаем блупринт
bp_posts = Blueprint("bp_posts", __name__, template_folder="templates")

post_dao = PostDAO(DATA_PATH_POST)
comments_dao = CommentDAO(DATA_PATH_COMMENTS)


@bp_posts.route("/")
def page_posts_index():
    """Главная страница со всеми постами"""
    all_posts = post_dao.get_posts_all()
    return render_template("index.html", posts=all_posts)


@bp_posts.route("/post/<int:pk>/")
def page_post_single(pk: int):
    """Страница с определенным постом"""
    post = post_dao.get_post_by_pk(pk)
    comments = comments_dao.get_comments_by_post_id(pk)
    comments_len = len(comments)

    if post is None:
        abort(404)

    return render_template("post_single.html", post=post, comments=comments, comments_len=comments_len)


@bp_posts.route("/users/<user_name>")
def page_posts_by_user(user_name: str):
    """Возвращает посты пользователя"""
    posts = post_dao.get_posts_by_user(user_name)

    if not posts:
        abort(404, "Такого пользователя не существует")

    return render_template("user-feed.html", posts=posts, user_name=user_name)


@bp_posts.route("/search/")
def page_search_posts():
    """Возвращает результаты поиска"""
    s = request.args.get("s", "")

    if s == "":
        posts = []
    else:
        posts = post_dao.search_for_posts(s)
    return render_template("search.html", s=s, posts=posts, posts_len=len(posts))
