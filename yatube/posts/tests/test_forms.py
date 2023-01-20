import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Comment, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Author')
        cls.group = Group.objects.create(slug='test-slug')
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.author = Client()
        self.author.force_login(PostFormTests.user)

    def test_create_new_post_in_database(self):
        """При отправке валидной формы со страницы создания поста
        создаётся новая запись в базе данных.
        """
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Текст из формы',
            'group': PostFormTests.group.pk,
            'image': uploaded,
        }
        self.author.post(
            reverse('posts:post_create'),
            data=form_data
        )
        new_post = Post.objects.filter(
            text='Текст из формы',
            group=PostFormTests.group.pk,
            author=self.user.pk,
            image='posts/small.gif',
        ).exists()
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(new_post)

    def test_edit_post_in_database(self):
        """При отправке валидной формы со страницы редактирования поста
        происходит изменение поста с post_id в базе данных.
        """
        form_data = {
            'text': 'Новый текст из формы',
            'group': PostFormTests.group.pk,
        }
        self.author.post(
            reverse(
                'posts:posts_edit',
                kwargs={'post_id': PostFormTests.post.pk}
            ),
            data=form_data,
        )
        new_text = Post.objects.get(pk=PostFormTests.post.pk).text
        new_group = Post.objects.get(pk=PostFormTests.post.pk).group
        self.assertEqual(new_text, 'Новый текст из формы')
        self.assertEqual(new_group, PostFormTests.group)

    def test_create_new_post_anonymous_in_database(self):
        """При отправке валидной формы
        со страницы создания поста неавторизованным пользователем
        новая запись в базе данных не создается.
        """
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст из формы',
            'group': PostFormTests.group,
        }
        self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data
        )
        self.assertEqual(Post.objects.count(), posts_count)

    def test_create_new_comment_in_database(self):
        """При отправке валидной формы
        со страницы деталей поста
        новый комментарий создается в базе данных.
        """
        comments_count = Comment.objects.count()
        form_data = {
            'text': 'Текс комментария'
        }
        self.author.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': PostFormTests.post.pk}
            ),
            data=form_data
        )
        self.assertEqual(Comment.objects.count(), comments_count + 1)

    def test_create_new_comment_anonymous_in_database(self):
        """При отправке валидной формы
        со страницы деталей поста неавторизованным пользователем
        новый комментарий не создается в базе данных.
        """
        comments_count = Comment.objects.count()
        form_data = {
            'text': 'Текс комментария'
        }
        self.guest_client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': PostFormTests.post.pk}
            ),
            data=form_data
        )
        self.assertEqual(Comment.objects.count(), comments_count)
