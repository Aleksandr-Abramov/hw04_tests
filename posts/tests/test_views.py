from django.test import TestCase, Client
from django.urls import reverse
from django import forms
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site

from ..models import Post, Group, User


class ViewPageContextTest(TestCase):

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

        cls.creator_user = Client()
        cls.creator_user.force_login(cls.user1)

        cls.group = Group.objects.create(
            title="Заголовок группы",
            slug="slug-test",
            description="Описание группы"
        )

        cls.post = Post.objects.create(
            text="Текст поста.",
            group=cls.group,
            author=cls.user1
        )

        site = Site(pk=1, domain='localhost:8000', name='localhost:8000')
        site.save()

        cls.flat_about = FlatPage.objects.create(
            url=reverse("about"),
            title="flat_about title",
            content="flat content"
        )

        cls.flat_terms = FlatPage.objects.create(
            url=reverse("terms"),
            title="flat_term title",
            content="flat content"
        )

        cls.flat_about.sites.add(site)
        cls.flat_terms.sites.add(site)

        cls.page_urls = {
            reverse("index"): "index.html",
            reverse("group_posts", kwargs={"slug": cls.group.slug}): "group.html",
            reverse("new_post"): "new.html",
            reverse("about"): "flatpages/default.html",
            reverse("terms"): "flatpages/default.html"
        }

    def test_templates_all_pages(self):
        """Тест шаблонов"""
        for page, templates in self.page_urls.items():
            response = self.creator_user.get(page)
            self.assertTemplateUsed(response, templates,
                                    f"{page} не возвращает шаблон {templates}")

    def test_contest_index_page(self):
        """ Тест контент index.html"""
        response = self.creator_user.get(reverse("index"))
        self.assertEqual(response.context.get("page")[0].text, self.post.text)
        self.assertEqual(response.context.get("page")[0].author.username, self.post.author.username)
        self.assertEqual(response.context.get("page")[0].group.title, self.post.group.title)

    def test_context_group_page(self):
        """ Тест контент group.html"""
        response = self.creator_user.get(reverse("group_posts", args=[self.group.slug]))
        self.assertEqual(response.context.get("page")[0].text, self.post.text)
        self.assertEqual(response.context.get("page")[0].group, self.post.group)
        self.assertEqual(response.context.get("page")[0].author, self.post.author)
        self.assertEqual(response.context.get("group").title, self.group.title)
        self.assertEqual(response.context.get("group").slug, self.group.slug)
        self.assertEqual(response.context.get("group").description, self.group.description)

    def test_content_new(self):
        """Тесе контент new.html"""
        response = self.creator_user.get(reverse("new_post"))
        self.assertIsInstance(response.context.get("form").fields.get("text"), forms.fields.CharField)
        self.assertIsInstance(response.context.get("form").fields.get("group"), forms.fields.ChoiceField)

    def test_content_profile(self):
        """Тест кнотекст profile.html"""
        response = self.creator_user.get(reverse("profile", kwargs={"username": self.user1.username}))
        self.assertEqual(response.context.get("page")[0].text, self.post.text)
        self.assertEqual(response.context.get("page")[0].author, self.post.author)
        self.assertEqual(response.context.get("page")[0].group, self.post.group)
        self.assertEqual(response.context.get("author_posts").username, self.user1.username)

    def test_context_post(self):
        """Тест контекст post.html"""
        response = self.creator_user.get(
            reverse("post", kwargs={"username": self.user1.username, "post_id": self.post.id}))
        self.assertEqual(response.context.get("author_posts").username, self.user1.username)
        self.assertEqual(response.context.get("number_post").text, self.post.text)
        self.assertEqual(response.context.get("number_post").author, self.post.author)
        self.assertEqual(response.context.get("number_post").group, self.post.group)

    def test_context_post_edit(self):
        """Тест контекст post_new.html"""
        response = self.creator_user.get(
            reverse("post_edit", kwargs={"username": self.user1.username, "post_id": self.post.id}))
        self.assertIsInstance(response.context.get("form").fields.get("text"), forms.fields.CharField)
        self.assertIsInstance(response.context.get("form").fields.get("group"), forms.fields.ChoiceField)

    def test_flat_about(self):
        """Тест контекст flatpages default.html"""
        response = self.creator_user.get(reverse("about"))
        self.assertEqual(response.context.get("flatpage").url, self.flat_about.url)
        self.assertEqual(response.context.get("flatpage").title, self.flat_about.title)
        self.assertEqual(response.context.get("flatpage").content, self.flat_about.content)

    def test_flat_terms(self):
        """Тест контекст flatpages default.html"""
        response = self.creator_user.get(reverse("terms"))
        self.assertEqual(response.context.get("flatpage").url, self.flat_terms.url)
        self.assertEqual(response.context.get("flatpage").title, self.flat_terms.title)
        self.assertEqual(response.context.get("flatpage").content, self.flat_terms.content)

    def test_create_content_index(self):
        """Тест создания поста index.html"""
        new_post = Post.objects.create(
            text="тестовый текст",
            author=self.user1,
            group=self.group
        )
        response = self.creator_user.get(reverse("index"))
        self.assertContains(response, new_post)

    def test_create_content_group(self):
        """Тест создания поста group.html"""
        new_post = Post.objects.create(
            text="тестовый текст",
            author=self.user1,
            group=self.group
        )
        response = self.creator_user.get(reverse("group_posts", args=["slug-test"]))
        self.assertContains(response, new_post)


class PaginatorViewsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(username="Alex")
        Group.objects.create(
            title="Название группы",
            slug="test-slug",
            description="тестовый текст"
        )
        cls.group = Group.objects.get(id=1)
        for i in range(13):
            Post.objects.create(
                text="Тестовый текст" + f" {i}",
                author=user,
                group=cls.group
            )

    def setUp(self):
        self.guest_client = Client()

    def test_index_first_page_contains_ten_records(self):
        """Тест пагинатор, записей на 1 странице  10"""
        response = self.guest_client.get(reverse("index"))
        self.assertEqual(len(response.context.get("page").object_list), 10,
                         "Количество записей не равняется 10")

    def test_index_second_page_contains_three_records(self):
        """Тест пагинатор, записей на 2 странице  3"""
        response = self.guest_client.get((reverse("index") + "?page=2"))
        self.assertEqual(len(response.context.get("page").object_list), 3,
                         "Количество записей не равняется 3")

    def test_group_first_page_contains_ten_records(self):
        """Тест пагинатор, записей на 1 странице  10"""
        response = self.guest_client.get(reverse(
            "group_posts",
            kwargs={"slug": "test-slug"}))
        self.assertEqual(len(response.context.get("page").object_list), 10)

    def test_group_second_page_contains_three_records(self):
        """Тест пагинатор, записей на 2 странице  3"""
        response = self.guest_client.get(reverse(
            "group_posts",
            kwargs={"slug": "test-slug"}) + "?page=2")
        self.assertEqual(len(response.context.get("page").object_list), 3)
