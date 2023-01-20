from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_not_author = User.objects.create(username='NotAuthor')
        cls.user_author = User.objects.create(username='Author')
        cls.group = Group.objects.create(slug='test-slug')
        cls.post = Post.objects.create(author=cls.user_author)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user_not_author)
        self.author = Client()
        self.author.force_login(PostURLTests.user_author)

    def test_url_exists_at_desired_location_anonymous(self):
        """Страницы
        /,
        /group/<slug:slug>/,
        /profile/<str:username>/,
        /posts/<int:post_id>/
        доступны любому пользователю.
        """
        list_of_url = [
            reverse('posts:index'),
            reverse(
                'posts:group_list',
                kwargs={'slug': PostURLTests.group.slug}
            ),
            reverse(
                'posts:profile',
                kwargs={'username': PostURLTests.user_author.username}
            ),
            reverse(
                'posts:posts_detail',
                kwargs={'post_id': PostURLTests.post.pk}
            ),
        ]
        for url in list_of_url:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_url_exists_at_desired_location_authorized_user(self):
        """Страница /create/ доступна любому авторизованному пользователю."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_edit_url_exists_at_desired_location_author(self):
        """Страница /posts/<int:post_id>/edit/ доступна автору."""
        response = self.author.get(
            reverse(
                'posts:posts_edit',
                kwargs={'post_id': PostURLTests.post.pk}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_non_existent_url_returns_404_error(self):
        """Несуществующая cтраница /unexisting_page/ возвращает ошибку 404."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_post_create_url_redirect_anonymous_on_admin_login(self):
        """Страница по адресу /create/ перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get(
            reverse('posts:post_create'), follow=True
        )
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_posts_edit_url_redirect_not_author_on_posts_detail(self):
        """Страница по адресу /posts/<int:post_id>/edit/
        перенаправит любого пользователя, кроме автора,
        на страницу деталей поста.
        """
        response = self.authorized_client.get(
            reverse(
                'posts:posts_edit',
                kwargs={'post_id': PostURLTests.post.pk}
            ),
            follow=True
        )
        self.assertRedirects(response, f'/posts/{PostURLTests.post.pk}/')

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': PostURLTests.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': PostURLTests.user_author.username}
            ): 'posts/profile.html',
            reverse(
                'posts:posts_detail',
                kwargs={'post_id': PostURLTests.post.pk}
            ): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:posts_edit',
                kwargs={'post_id': PostURLTests.post.pk}
            ): 'posts/create_post.html',
        }

        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.author.get(address)
                self.assertTemplateUsed(response, template)

    def test_404_uses_correct_template(self):
        """Cтраница 404 отдаёт кастомный шаблон."""
        response = self.author.get('/unexisting_page/')
        self.assertTemplateUsed(response, 'core/404.html')
