from django.test import TestCase

from posts.models import Group, Post, User


class PostsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_object_name_is_text_fild(self):
        """__str__  post - это строчка с содержимым post.text."""
        post = PostsModelTest.post
        expected_object_name_of_post = post.text
        self.assertEqual(expected_object_name_of_post, str(post))

    def test_verbose_name(self):
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

    def test_help_text(self):
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

    def test_object_name_is_title_fild(self):
        """__str__  group - это строчка с содержимым group.title."""
        group = PostsModelTest.group
        expected_object_name_of_group = group.title
        self.assertEqual(expected_object_name_of_group, str(group))
