from django.test import TestCase, Client
from ..models import Group, Post, User
from django.contrib.auth import get_user_model
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.urls import reverse


class StaticURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(username="dima")
        Group.objects.create(
            title="Название группы",
            slug="test-slug",
            description="тестовый текст"
        )
        cls.group = Group.objects.get(id=1)

        Post.objects.create(
            text="Тестовый текст",
            author=cls.user,
            group=cls.group
        )
        cls.post = Post.objects.get(id=1)

        cls.page_urls = {
            "/": "index.html",
            "/new/": "new.html",
            "/group/{}/".format(StaticURLTests.group.slug): "group.html",
            "/{}/".format(str(StaticURLTests.user)): "profile.html",
            "/{}/{}/".format(str(StaticURLTests.user), StaticURLTests.post.id): "post.html",
            # "/about/about-author/": "flatpages/default.html",
            # "/about-spec/": "flatpages/default.html"
        }



    def setUp(self):
        self.user = get_user_model().objects.create_user(username="Alex")
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.page = FlatPage.objects.create(
            url="/about-author/",
            title="Об авторе",
        )

    def test_flat(self):

        response = self.authorized_client.get(self.page.url)
        print(response.status_code, response.content)
        # response = self.guest_client.get("/absout-author/")
        # response = self.guest_client.get(self.about_author.url)
        self.assertEqual(response.status_code, 200, "Ошибка")


    def test_available_pages(self):
        # Тест доступности страниц для авторизованного пользователя.
        for page, template in StaticURLTests.page_urls.items():
            response = self.authorized_client.get(page)
            self.assertEqual(response.status_code, 200,
                             "Зарегистрированный пользователь, не смог войти.")

        for page, template in StaticURLTests.page_urls.items():
            # Тест доступности страниц для неавторизованного пользователя.
            response = self.guest_client.get(page)
            self.assertEqual(response.status_code, 200,
                             "Незарегистрированный пользователь, не смог войти.")





    def test_page_templates(self):
        # Тест, шаблон с данным именем используется при рендеренге.
        for page, template in StaticURLTests.page_urls.items():
            with self.subTest():
                response = self.authorized_client.get(page)
                self.assertTemplateUsed(response, template,
                                        "{} данный шаблон не работает".format(template))
#
#     # Редирект
#     # def test_static_new_page_redirect(self):
#     #     response = self.guest_client.get('/new/', follow=True)
#     #     self.assertRedirects(response, '/new/?next=/index/')
