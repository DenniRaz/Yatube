import shutil
import tempfile

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Follow, Group, Post, User

NUM_OF_POSTS = 15
POSTS_FIRST_PAGE = 10
POSTS_SECOND_PAGE = 5
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPageTest(TestCase):
    @classmethod
    def setUpClass(cls):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        super().setUpClass()
        cls.user = User.objects.create(username='Author')
        cls.client = User.objects.create(username='Client')
        cls.client_2 = User.objects.create(username='Client_2')
        cls.group = Group.objects.create(slug='test-slug')
        cls.post = Post.objects.create(
            group=cls.group,
            text='Тестовый пост',
            author=cls.user,
            image=cls.uploaded
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.author = Client()
        self.author.force_login(PostPageTest.user)
        self.authorized_client = Client()
        self.authorized_client.force_login(PostPageTest.client)
        self.authorized_client_2 = Client()
        self.authorized_client_2.force_login(PostPageTest.client_2)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': PostPageTest.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': PostPageTest.user.username}
            ): 'posts/profile.html',
            reverse(
                'posts:posts_detail',
                kwargs={'post_id': PostPageTest.post.pk}
            ): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:posts_edit',
                kwargs={'post_id': PostPageTest.post.pk}
            ): 'posts/create_post.html',
        }

        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.author.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index с адресом posts:index
        сформирован с правильным контекстом.
        """
        response = self.author.get(reverse('posts:index'))
        first_object = {
            response.context['page_obj'][0].group: PostPageTest.group,
            response.context['page_obj'][0].text: 'Тестовый пост',
            response.context['page_obj'][0].author: PostPageTest.user,
            response.context['page_obj'][0].image.name: 'posts/small.gif',
        }
        for value, expected in first_object.items():
            with self.subTest(expected=expected):
                self.assertEqual(value, expected)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list с адресом posts:group_list
        сформирован с правильным контекстом.
        """
        response = self.author.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': PostPageTest.group.slug}
            )
        )
        first_object = {
            response.context['page_obj'][0].group: PostPageTest.group,
            response.context['page_obj'][0].text: 'Тестовый пост',
            response.context['page_obj'][0].author: PostPageTest.user,
            response.context['page_obj'][0].image.name: 'posts/small.gif'
        }
        for value, expected in first_object.items():
            with self.subTest(expected=expected):
                self.assertEqual(value, expected)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile с адресом posts:profile
        сформирован с правильным контекстом.
        """
        response = self.author.get(
            reverse(
                'posts:profile',
                kwargs={'username': PostPageTest.user.username}
            )
        )
        first_object = {
            response.context['page_obj'][0].group: PostPageTest.group,
            response.context['page_obj'][0].text: 'Тестовый пост',
            response.context['page_obj'][0].author: PostPageTest.user,
            response.context['page_obj'][0].image.name: 'posts/small.gif'
        }
        for value, expected in first_object.items():
            with self.subTest(expected=expected):
                self.assertEqual(value, expected)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail с адресом posts:posts_detail
        сформирован с правильным контекстом.
        """
        response = self.author.get(
            reverse(
                'posts:posts_detail',
                kwargs={'post_id': PostPageTest.post.pk}
            )
        )
        first_object = {
            response.context['post'].group: PostPageTest.group,
            response.context['post'].text: 'Тестовый пост',
            response.context['post'].author: PostPageTest.user,
            response.context['post'].image.name: 'posts/small.gif'
        }
        for value, expected in first_object.items():
            with self.subTest(expected=expected):
                self.assertEqual(value, expected)

    def test_create_post_page_show_correct_context(self):
        """Шаблон create_post с адресом posts:post_create
        сформирован с правильным контекстом.
        """
        response = self.author.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_create_post_for_edit_page_show_correct_context(self):
        """Шаблон create_post с адресом posts:posts_edit
        сформирован с правильным контекстом.
        """
        response = self.author.get(
            reverse(
                'posts:posts_edit',
                kwargs={'post_id': PostPageTest.post.pk}
            )
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_added_correctly(self):
        """Пост при создании добавлен корректно"""
        response_index = self.author.get(reverse('posts:index'))
        response_group_list = self.author.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': PostPageTest.group.slug}
            )
        )
        response_profile = self.author.get(
            reverse(
                'posts:profile',
                kwargs={'username': PostPageTest.user.username}
            )
        )
        context = [
            response_index.context['page_obj'],
            response_group_list.context['page_obj'],
            response_profile.context['page_obj'],
        ]
        for objects in context:
            with self.subTest(objects=objects):
                self.assertIn(PostPageTest.post, objects)

    def test_post_another_group(self):
        """Пост не попал в другую группу"""
        group_2 = Group.objects.create(slug='test-slug-2')
        response_2 = self.author.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': group_2.slug}
            )
        )
        objects = response_2.context['page_obj']
        self.assertNotIn(PostPageTest.post, objects)

    def test_cache_index(self):
        """Проверка кеширования для страницы index."""
        response = self.author.get(reverse('posts:index'))
        posts = response.content
        Post.objects.create(
            text='Тестовый текст',
            author=PostPageTest.user,
        )
        response_start = self.author.get(reverse('posts:index'))
        posts_start = response_start.content
        cache.clear()
        response_finish = self.author.get(reverse('posts:index'))
        posts_finish = response_finish.content
        self.assertEqual(posts, posts_start)
        self.assertNotEqual(posts, posts_finish)

    def test_follow_and_unfollow(self):
        """Авторизованный пользователь может подписываться на
        других пользователей и удалять их из подписок.
         """
        self.authorized_client.post(
            reverse(
                'posts:profile_follow',
                kwargs={'username': PostPageTest.user.username}
            )
        )
        follow = Follow.objects.filter(
            user=PostPageTest.client,
            author=PostPageTest.user,
        ).exists()
        self.authorized_client.post(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': PostPageTest.user.username}
            )
        )
        unfollow = Follow.objects.filter(
            user=PostPageTest.client,
            author=PostPageTest.user,
        ).exists()
        self.assertTrue(follow)
        self.assertFalse(unfollow)

    def test_add_follow_correctly(self):
        """Новая запись пользователя появляется в ленте тех,
        кто на него подписан
        и не появляется в ленте тех, кто не подписан.
        """
        self.authorized_client.post(
            reverse(
                'posts:profile_follow',
                kwargs={'username': PostPageTest.user.username}
            )
        )
        post = Post.objects.create(
            text='Тестовый текст для подписки',
            author=PostPageTest.user,
        )
        response = self.authorized_client.get(
            reverse('posts:follow_index')
        )
        follow_post = response.context['page_obj']
        response_2 = self.authorized_client_2.get(
            reverse('posts:follow_index')
        )
        follow_post_2 = response_2.context['page_obj']
        self.assertIn(post, follow_post)
        self.assertNotIn(post, follow_post_2)

    def test_subscrib_to_yourself_does_not_happen(self):
        """Подписка на самого не себя не происходит."""
        self.author.post(
            reverse(
                'posts:profile_follow',
                kwargs={'username': PostPageTest.user.username}
            )
        )
        follow = Follow.objects.filter(
            user=PostPageTest.user,
            author=PostPageTest.user,
        ).exists()
        self.assertFalse(follow)


class PostPaginatorTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Author')
        cls.group = Group.objects.create(slug='test-slug')
        for num_post in range(NUM_OF_POSTS):
            Post.objects.create(
                group=cls.group,
                author=cls.user,
            )

    def setUp(self):
        self.author = Client()
        self.author.force_login(PostPaginatorTest.user)

    def test_first_page_contains_ten_records(self):
        """На первую старницу выведено нужное количество постов"""
        urls_names = [
            reverse('posts:index'),
            reverse(
                'posts:group_list',
                kwargs={'slug': PostPaginatorTest.group.slug}
            ),
            reverse(
                'posts:profile',
                kwargs={'username': PostPaginatorTest.user.username}
            ),
        ]
        for url_name in urls_names:
            with self.subTest(url_name=url_name):
                response = self.author.get(url_name)
                num_posts = len(response.context['page_obj'])
                self.assertEqual(num_posts, POSTS_FIRST_PAGE)

    def test_second_page_contains_ten_records(self):
        """На вторую старницу выведено нужное количество постов"""
        urls_names = [
            reverse('posts:index'),
            reverse(
                'posts:group_list',
                kwargs={'slug': PostPaginatorTest.group.slug}
            ),
            reverse(
                'posts:profile',
                kwargs={'username': PostPaginatorTest.user.username}
            ),
        ]
        for url_name in urls_names:
            with self.subTest(url_name=url_name):
                response = self.author.get(url_name + '?page=2')
                num_posts = len(response.context['page_obj'])
                self.assertEqual(num_posts, POSTS_SECOND_PAGE)
