from django.test import TestCase, Client
from ..models import Group, Post, User
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.urls import reverse


class StaticURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user1 = User.objects.create(
            username="leo",
            first_name="leo",
            last_name="abramov"
        )
        cls.user2 = User.objects.create(
            username="alex",
            first_name="alex",
            last_name="abramov"
        )
        cls.guest_client = Client()
        cls.creator_user = Client()
        cls.creator_user.force_login(cls.user1)
        cls.authorized_user = Client()
        cls.authorized_user.force_login(cls.user2)

        cls.group = Group.objects.create(
            title="Заголовок группы",
            slug="test-slug",
            description="Тестовый текст группы"
        )

        cls.post = Post.objects.create(
            text="Текст Post",
            author=cls.user1,
            group=cls.group
        )

        site = Site(pk=1, domain='localhost:8000', name='localhost:8000')
        site.save()

        cls.flat_about = FlatPage.objects.create(
            url=reverse("about"),
            title="about me",
            content="<b>some content</b>"
        )

        cls.flat_terms = FlatPage.objects.create(
            url=reverse("terms"),
            title="about terms",
            content="some contet"
        )

        cls.flat_about.sites.add(site)
        cls.flat_terms.sites.add(site)

        cls.list_pages = {
            reverse("index"): "index.html",
            reverse("new_post"): "new.html",
            reverse("group_posts",
                    kwargs={"slug": cls.group.slug}): "group.html",
            reverse("profile",
                    kwargs={"username": cls.user1.username}): "profile.html",
            reverse("post",
                    kwargs={"username": cls.user1.username, "post_id": cls.post.id}): "post.html",
            reverse("about"): "flatpages/default.html",
            reverse("terms"): "flatpages/default.html"
        }

    def test_other_pages_guest_client_status_code_200(self):
        """Проверки страниц код 200"""
        for page, template in self.list_pages.items():
            response = self.guest_client.get(page)
            self.assertEqual(response.status_code, 200,
                             f"Страница {page} не отвечает")

    def test_other_pages_authorized_client_status_code_200(self):
        for page, template in self.list_pages.items():
            response = self.guest_client.get(page)
            self.assertEqual(response.status_code, 200,
                             f"Страница {page} не отвечает")

    def test_other_pages_guest_client_templates(self):
        """Проверка шаблонов"""
        for page, template in self.list_pages.items():
            response = self.guest_client.get(page)
            self.assertTemplateUsed(response, template,
                                    f"{page} шаблон {template} не работает")

    def test_other_pages_authorized_user_templates(self):
        for page, template in self.list_pages.items():
            response = self.authorized_user.get(page)
            self.assertTemplateUsed(response, template,
                                    f"{page} шаблон {template} не работает")

    def test_post_edit_guest_client_200(self):
        """Проверки для страницы post_edit(post_new.html)"""
        response = self.guest_client.get(
            reverse("post_edit",
                    kwargs={"username": self.user1.username,
                            "post_id": 1}), follow=True)
        self.assertEqual(response.status_code, 200,
                         "post_edit пользователь гость не может зайти.")

    def test_post_edit_authorized_user_200(self):
        response = self.authorized_user.get(
            reverse("post_edit",
                    kwargs={"username": self.user1.username,
                            "post_id": 1}), follow=True)
        self.assertEqual(response.status_code, 200,
                         "post_edit авторизованный пользователь не может зайти.")

    def test_post_edit_creator_user_200(self):
        response = self.creator_user.get(
            reverse("post_edit",
                    kwargs={"username": self.user1.username,
                            "post_id": 1}), follow=True)
        self.assertEqual(response.status_code, 200,
                         "post_edit неавторизованный пользователь не может зайти.")

    def test_post_edit_template(self):
        response = self.creator_user.get(
            reverse("post_edit",
                    kwargs={"username": self.user1.username,
                            "post_id": 1}))
        self.assertTemplateUsed(response, "post_new.html",
                                "post_edit не возвращает post_new.html")

    def test_post_edit_authorized_user_redirect(self):
        response = self.authorized_user.get(
            reverse("post_edit",
                    kwargs={"username": self.user1.username,
                            "post_id": 1}))
        self.assertRedirects(
            response,
            f"/{self.user1.username}/{self.post.id}/")

    def test_post_edit_guest_client_redirect(self):
        response = self.guest_client.get(
            reverse(
                "post_edit",
                kwargs={"username": self.user1.username,
                        "post_id": 1}))
        self.assertRedirects(
            response,
            reverse("post",
                    kwargs={"username": self.user1.username,
                            "post_id": self.post.id}))
