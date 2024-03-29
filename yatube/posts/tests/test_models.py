from django.test import TestCase

from ..models import (
    COMMENT_STR,
    Comment,
    FOLLOW_STR,
    Follow,
    Group,
    POST_STR,
    Post,
    User,
)


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.user_follower = User.objects.create_user(username='user_follower')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
        )
        cls.comment = Comment.objects.create(
            author=cls.user,
            text='Тестовый комментарий',
            post=cls.post,
        )
        cls.follow = Follow.objects.create(
            author=cls.user,
            user=cls.user_follower,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        models_str = [
            (POST_STR.format(
                author=self.post.author.username,
                group=self.post.group,
                text=self.post.text,
            ), self.post),
            (self.group.title, self.group),
            (FOLLOW_STR.format(
                user=self.follow.user.username,
                author=self.follow.author.username,
            ), self.follow),
            (COMMENT_STR.format(
                author=self.comment.author.username,
                text=self.comment.text,
            ), self.comment),
        ]
        for str_method, model in models_str:
            with self.subTest():
                self.assertEqual(str_method, str(model))
