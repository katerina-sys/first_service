import pytest

from bp_posts.dao.post import Post
from bp_posts.dao.post_dao import PostDAO


def check_field(post):
    fields = ["poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"]

    for field in fields:
        assert hasattr(post, field), f"Нет поля {field}"


class TestPostsDAO:

    # ТЕСТЫ ПОЛУЧЕНИЯ ВСЕГО

    @pytest.fixture
    def post_dao(self):
        post_dao_instance = PostDAO("post_mock.json")
        return post_dao_instance

    def test_get_all(self, post_dao):
        posts = post_dao.get_posts_all()
        assert type(posts) == list, "Incorrect type for result"

        post = post_dao.get_posts_all()[0]
        assert type(post) == Post, "Incorrect type for result single item"

    def test_get_all_fields(self, post_dao):
        posts = post_dao.get_posts_all()
        post = post_dao.get_posts_all()[0]

        check_field(post)

    # ТЕСТЫ ПОЛУЧЕНИЯ ПО ID

    def test_correct_id(self, post_dao):
        posts = post_dao.get_posts_all()

        correct_pk = {1, 2, 3}
        pks = set([post.pk for post in posts])
        assert pks == correct_pk, "Не совпадают введенные id"

    def test_get_by_pk_types(self, post_dao):
        post = post_dao.get_post_by_pk(1)
        assert type(post) == Post, "Incorrect type for result single item"

    def test_get_by_pk_fields(self, post_dao):
        post = post_dao.get_post_by_pk(1)
        check_field(post)

    def test_get_by_pk_none(self, post_dao):
        post = post_dao.get_post_by_pk(0)
        assert post is None, "Should be None for non existent pk"

    @pytest.mark.parametrize("pk", [1, 2, 3])
    def test_get_by_pk_correct_id(self, post_dao, pk):
        post = post_dao.get_post_by_pk(pk)
        assert post.pk == pk, f"Incorrect post.pk for requesten post with pk = {pk}"

    # ТЕСТЫ ПОИСКОВОЙ СИСТЕМЫ

    def test_search_in_content_types(self, post_dao):
        posts = post_dao.search_for_posts("ага")
        assert type(posts) == list, "Incorrect type for result"

        post = post_dao.get_posts_all()[0]
        assert type(post) == Post, "Incorrect type for result single item"

    def test_search_in_content_fields(self, post_dao):
        posts = post_dao.search_for_posts("ага")
        post = post_dao.get_posts_all()[0]
        check_field(post)
        assert type(post) == Post, "Incorrect type for result single item"

    def test_search_in_content_not_found(self, post_dao):
        posts = post_dao.search_for_posts("а2345345342")
        assert posts == [], "Should be [] for not substring not found"

    @pytest.mark.parametrize("s, expected_pk", [
        ("Ага", {1}),
        ("Вышел", {2}),
        ("на", {1, 2, 3}),
    ])
    def test_search_content_result(self, post_dao, s, expected_pk):
        posts = post_dao.search_for_posts(s)
        pks = set([post.pk for post in posts])
        assert pks == expected_pk, f"Incorrect results searching for {s}"

    # ТЕСТЫ ПОЛУЧЕНИЯ ИМЕНИ АВТОРА

    def test_poster_name(self, post_dao):
        poster_name = post_dao.get_posts_by_user("leo")
        assert type(poster_name) == list, "Incorrect type for result"

    def test_poster_name_not_found(self, post_dao):
        poster_name = post_dao.get_posts_by_user("asdf2342sf")
        assert poster_name == [], "Should be [] for not substring not found"


