import json
from json import JSONDecodeError

from bp_posts.dao.comment import Comment
from exceptions.all_exceptions import DataSourceError


class CommentDAO:

    def __init__(self, path):
        self.path = path

    def _load_data(self):
        """Загружает данные из файла"""
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                posts_data = json.load(file)
        except(FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f'Не удается получить данные из файла {self.path}')

        return posts_data

    def load_comments(self):
        """Возвращает список экзмепляров Comment"""
        comments_data = self._load_data()

        list_of_posts = [Comment(**comment_data) for comment_data in comments_data]

        return list_of_posts

    def get_comments_by_post_id(self, post_pk):
        """Возвращает комментарии определенного поста"""
        comments = self.load_comments()
        all_comments = []
        for comment in comments:
            if comment.post_pk == post_pk:
                all_comments.append(comment)
        return all_comments


#cd = CommentDAO("../../data/comments.json")

#print(cd.get_comments_by_post_id(2))
