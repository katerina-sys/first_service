import pytest
import requests

import bp_api.views


class TestApi:
    post_keys = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}

    def test_all_posts_correct_status_code(self):
        """Тест стаус-код для всех постов"""
        response = requests.get("http://127.0.0.1:5000/api/posts")
        assert response.status_code == 200

    def test_all_posts_has_correct_keys(self):
        """Тест на проверку всех ключей у постов"""
        result = requests.get("http://127.0.0.1:5000/api/posts")
        list_of_posts = result.json()

        for post in list_of_posts:
            assert post.keys() == self.post_keys, "Неверные ключи у полученного словаря"

    def test_single_post_correct_status(self):
        """Тест стаус-код для одного поста"""
        result = requests.get("http://127.0.0.1:5000/api/posts/1/")
        assert result.status_code == 200

    def test_post_is_none_correct_status_404(self):
        """Статус код несуществующего поста"""
        result = requests.get("http://127.0.0.1:5000/api/posts/0/")
        assert result.status_code == 404

    def test_single_post_has_correct_keys(self):
        """Тест на проверку всех ключей у поста"""
        result = requests.get("http://127.0.0.1:5000/api/posts/1/")
        post = result.json()
        post_keys = set(post.keys())
        assert post_keys == self.post_keys
