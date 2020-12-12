from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Post, Group
from ..forms import PostForm


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
    # Тест соханения данных и redirect
    def test_new_post_create_post_end_redirect(self):
        from_data = {
            "group": self.group.id,
            "text": "Тестовый текст",
        }
        number_posts = Post.objects.count()
        response = self.authorized_user.post(reverse("new_post"), data=from_data, follow=True)
        self.assertEqual(response.status_code, 200, "Страница new.html не отвечает")
        self.assertEqual(Post.objects.count(), number_posts+1, "Количество постов меньше 1")
        self.assertRedirects(response, "/")



    # @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()
    #     Group.objects.create(
    #         title="Лев толстой",
    #         slug="test-slug",
    #         description="Тестовое описание"
    #     )
    #     cls.group = Group.objects.get(id=1)
    #     cls.form = PostForm()
    #
    # def setUp(self):
    #     self.user = get_user_model().objects.create_user(username="test-user")
    #     self.authenticated_user = Client()
    #     self.authenticated_user.force_login(self.user)
    #
    # def test_create_post_and_redirect(self):
    #     from_data = {
    #         "group": self.group.id,
    #         "text": "Тестовый текст",
    #     }
    #     tasks_count = Post.objects.count()
    #     print(print(tasks_count))
    #     response = self.authenticated_user.post(
    #         reverse("new_post"),
    #         data=from_data,
    #         follow=True
    #     )
    #     print(print(tasks_count))
    #     self.assertEqual(Post.objects.count(), tasks_count + 1)
    #     print(Post.objects.count())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertRedirects(response, "/")
    #
    # def test_update_post_and_redirect(self):
    #
    #
    # def test_form_field_help_text(self):
    #     title_help_text = self.form.fields["text"].help_text
    #     self.assertEqual(title_help_text, "Поле для хранения произвольного текста")
    #
    # def test_form_field_label(self):
    #     title_label = self.form.fields["text"].label
    #     self.assertEqual(title_label, "Текст поста")
