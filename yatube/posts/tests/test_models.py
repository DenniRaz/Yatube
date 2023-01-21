from django.test import TestCase

from posts.models import Comment, Follow, Group, Post, User


class PostsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.client = User.objects.create_user(username='TestUser_2')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Тестовый комментарий',
        )
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.client,
        )

    def test_object_name_is_title_fild(self):
        """__str__  group - это строчка с содержимым group.title."""
        group = PostsModelTest.group
        expected_object_name_of_group = group.title
        self.assertEqual(expected_object_name_of_group, str(group))

    def test_object_name_is_text_fild(self):
        """__str__  post - это строчка с содержимым post.text."""
        post = PostsModelTest.post
        expected_object_name_of_post = post.text
        self.assertEqual(expected_object_name_of_post, str(post))

    def test_verbose_name_post(self):
        """Verbose_name в полях post совпадает с ожидаемым."""
        post = PostsModelTest.post
        field_verbose_name = {
            'group': 'Группа',
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
        }
        for field, expected_value in field_verbose_name.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_verbose_name_comment(self):
        """Verbose_name в полях comment совпадает с ожидаемым."""
        post = PostsModelTest.comment
        field_verbose_name = {
            'post': 'Пост',
            'author': 'Автор',
            'text': 'Текст комментария',
            'created': 'Дата публикации комментария',
        }
        for field, expected_value in field_verbose_name.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_verbose_name_follow(self):
        """Verbose_name в полях follow совпадает с ожидаемым."""
        post = PostsModelTest.follow
        field_verbose_name = {
            'user': 'Подписчик',
            'author': 'Подписка',
        }
        for field, expected_value in field_verbose_name.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_help_text_post(self):
        """Help_text в полях post совпадает с ожидаемым."""
        post = PostsModelTest.post
        field_help_text = {
            'group': 'Группа, к которой будет относиться пост',
            'text': 'Введите текст поста',
        }
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)

    def test_help_text_comment(self):
        """Help_text в полях comment совпадает с ожидаемым."""
        post = PostsModelTest.comment
        field_help_text = {
            'text': 'Введите текс комментария',
        }
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)
