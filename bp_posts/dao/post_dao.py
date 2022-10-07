import json
from json import JSONDecodeError

from bp_posts.dao.post import Post
from exceptions.all_exceptions import DataSourceError


class PostDAO:

    def __init__(self, path):
        self.path = path

    def _load(self):
        """Загружает данные из файла"""
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                posts_data = json.load(file)
        except(FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f'Не удается получить данные из файла {self.path}')

        return posts_data

    def load_posts(self):
        """Возвращает список экзмепляров Post"""
        posts_data = self._load()

        list_of_posts = [Post(**post_data) for post_data in posts_data]

        return list_of_posts

    def get_posts_all(self):
        """Возвращает все посты"""
        all_posts = self.load_posts()
        return all_posts

    def get_post_by_pk(self, pk):
        """Возвращает один пост по его идентификатору"""

        if type(pk) != int:
            raise TypeError("pk must be int")

        posts = self.load_posts()
        for post in posts:
            if post.pk == pk:
                return post

    def search_for_posts(self, substring):
        """Возвращает список постов по ключевому слову"""
        substring = str(substring).lower()

        searching_posts = []
        posts = self.load_posts()
        for post in posts:
            if substring in post.content.lower():
                searching_posts.append(post)
        return searching_posts

    def get_posts_by_user(self, user_name):
        """Возвращает посты определенного пользователя"""
        user_name = str(user_name).lower()

        posts_found = []
        posts = self.load_posts()
        for post in posts:
            if post.poster_name.lower() == user_name:
                posts_found.append(post)
        return posts_found




