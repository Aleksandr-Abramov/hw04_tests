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

        site = Site(pk=1, domain='localhost:8000', name='localhost:8000')
        site.save()

        cls.flat_about = FlatPage.objects.create(
            url=reverse('about-author'),
            title='about me',
            content='<b>some content</b>')

        cls.flat_spec = FlatPage.objects.create(
            url=reverse('terms'),
            title='about me',
            content='<b>some content</b>'
        )
        cls.flat_about.sites.add(site)
        cls.flat_spec.sites.add(site)

        cls.page_urls = {
            "/": "index.html",
            "/new/": "new.html",
            "/group/{}/".format(StaticURLTests.group.slug): "group.html",
            "/{}/".format(str(StaticURLTests.user)): "profile.html",
            "/{}/{}/".format(str(StaticURLTests.user), StaticURLTests.post.id): "post.html",
            # "/{}/{}/edit".format(str(StaticURLTests.user), StaticURLTests.post.id): "post_new.html",
            reverse("about"): "flatpages/default.html",
            reverse("terms"): "flatpages/default.html",
            # "/about-spec/": "flatpages/default.html"
        }





    def setUp(self):
        self.user = get_user_model().objects.create_user(username="Alex")
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        # site = Site(pk=1, domain='localhost:8000', name='localhost:8000')
        # site.save()
        #
        # self.flat_about = FlatPage.objects.create(
        #     url=reverse('about-author'),
        #     title='about me',
        #     content='<b>some content</b>')
        #
        # self.flat_spec = FlatPage.objects.create(
        #     url=reverse('terms'),
        #     title='about me',
        #     content='<b>some content</b>'
        # )
        # self.flat_about.sites.add(site)
        # self.flat_spec.sites.add(site)

    # def test_flat_pages_response(self):
    #     """Проверяем доступность статических страниц"""
    #     for url in (reverse('about-author'), reverse('about-spec')):
    #         with self.subTest(url=url):
    #             response = self.guest_client.get(url)
    #             self.assertEqual(response.status_code, 200)
    #     response = self.guest_client.get(self.flat_about.url)
    #     self.assertEqual(response.status_code, 200, "Ошибка")


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



    # def test_page_templates(self):
    #     # Тест, шаблон с данным именем используется при рендеренге.
    #     for page, template in StaticURLTests.page_urls.items():
    #         with self.subTest():
    #             response = self.authorized_client.get(page)
    #             self.assertTemplateUsed(response, template,
    #                                     "{} данный шаблон не работает".format(template))
#
#     # Редирект
#     # def test_static_new_page_redirect(self):
#     #     response = self.guest_client.get('/new/', follow=True)
#     #     self.assertRedirects(response, '/new/?next=/index/')
