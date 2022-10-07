import logging

from flask import Blueprint, jsonify
from werkzeug.exceptions import abort

from bp_posts.dao.comment_dao import CommentDAO
from bp_posts.dao.post_dao import PostDAO
from config import DATA_PATH_POST, DATA_PATH_COMMENTS

# Создаем блупринт
bp_api = Blueprint("bp_api", __name__)

#Объекты доступа к данным
post_dao = PostDAO(DATA_PATH_POST)
comments_dao = CommentDAO(DATA_PATH_COMMENTS)

api_logger = logging.getLogger("api_logger")

@bp_api.route('/posts')
def api_all_posts():
    """Эндпоинт всех постов"""
    all_posts = post_dao.get_posts_all()
    api_logger.debug("Запрошены все посты")

    return jsonify([post.dict_post() for post in all_posts]), 200


@bp_api.route('/posts/<int:pk>/')
def api_single_post(pk: int):
    """Эндпоинт одного поста"""
    post = post_dao.get_post_by_pk(pk)
    if post is None:
        api_logger.debug(f"Обращение к несуществубщему посту {pk}")
        abort(404, "Таких данных не существует")

    api_logger.debug(f"Запрошен пост {pk}")

    return jsonify(post.dict_post()), 200
