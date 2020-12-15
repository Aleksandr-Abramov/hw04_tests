from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Post, Group


class PostFormTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(username="test-user")
        cls.authorized_user = Client()
        cls.authorized_user.force_login(cls.user)

        cls.group = Group.objects.create(
            title="Лев толстой",
            slug="test-slug",
            description="Тестовое описание"
        )

        cls.post = Post.objects.create(
            text="Текст поста.",
            group=cls.group,
            author=cls.user
        )

    def test_new_post_create_post_end_redirect(self):
        """Тест соханения данных и redirect для new_post"""
        from_data = {
            "group": self.group.id,
            "text": "Тестовый текст",
        }
        number_posts = Post.objects.count()
        response = self.authorized_user.post(
            reverse("new_post"),
            data=from_data,
            follow=True)
        self.assertEqual(
            response.status_code,
            200,
            "Страница new.html не отвечает")
        self.assertEqual(
            Post.objects.count(),
            number_posts + 1,
            "Количество постов меньше 1")
        self.assertRedirects(response, reverse("index"))

    def test_post_edit_create_post_end_redirect(self):
        """Тест соханения данных и redirect для post_edit"""
        from_data = {
            "group": self.group.id,
            "text": "Тестовый текст",
        }
        number_posts = Post.objects.count()
        response = self.authorized_user.post(
            reverse(
            "post_edit",
            args=[self.post.author, self.post.id]),
            data=from_data,
            follow=True)
        self.assertEqual(
            response.status_code,
            200,
            "Страница new.html не отвечает")
        # Максим, здравствуйте. Эта проверка из теории практикума. Так советует наставник.
        self.assertEqual(
            Post.objects.count(),
            number_posts + 1,
            "Количество постов меньше 1")
        self.assertRedirects(
            response,
            reverse("post", args=[self.post.author, self.post.id]))
