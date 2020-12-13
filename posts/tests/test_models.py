from django.test import TestCase
from ..models import Post, Group
from django.contrib.auth import get_user_model


class TestModelGroup(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Group.objects.create(
            title="Название группы",
            slug="test-slug",
            description="тестовый текст"
        )
        cls.group = Group.objects.get(id=1)

    def test_field_group_verbose_name(self):
        """Тест полей модели Group, на получение имени (verbose_name)"""
        group_field = self.group

        field_verbose = {
            "title": "Название группы:",
            "slug": "Адрес в интернете:",
            "description": "Информация о авторе."
        }

        for value, expect in field_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group_field._meta.get_field(value).verbose_name,
                    expect,
                    "verbose-name с ошибкой.")

    def test_field_group_help_text(self):
        """Тест полей модели Group, на получение вспапогательного текста (help_text)"""
        group_field = self.group

        field_help_text = {
            "title": "Введите название группы",
            "slug": ("Укажите адрес страницы, указывающий на группу. "
                     "Используйте латиницу, цифры, дефисы и знаки подчёркивания."),
            "description": "Справочная информация о авторе."
        }

        for value, expected in field_help_text.items():
            with self.subTest(value=value):
                self.assertEqual(group_field._meta.get_field(value).help_text,
                                 expected,
                                 "help-text с ошибкой.")

    def test_group_str_method(self):
        """Тест метода __str__(), модели Group"""
        value = self.group.__str__()
        expected = self.group.title
        self.assertEqual(value, expected, "__str__() не работает.")


class TestModelPost(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = get_user_model().objects.create_user(username="Alex")
        group = Group.objects.create(
            title="Название группы",
            slug="test-slug",
            description="тестовый текст"
        )

        Post.objects.create(
            text="Тестовый текст",
            author=user,
            group=group
        )
        cls.post = Post.objects.get(id=1)

    def test_field_group_verbose_name(self):
        """Тест полей модели Group, на получение имени (verbose_name)"""
        post_fields = self.post
        field_verbose = {
            "text": "Текст поста",
            "author": "Автор поста:",
            "group": "Автор:"
        }

        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(post_fields._meta.get_field(value).verbose_name,
                                 expected,
                                 "post.verbose_name c ошибкой.")

    def test_field_group_help_text(self):
        """Тест полей модели Post, на получение вспапогательного текста (help_text)"""
        post_fields = self.post

        field_verbose = {
            "text": "Поле для хранения произвольного текста",
            "author": "Пользователь опубликовавший пост.",
            "group": "Автор."
        }

        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(post_fields._meta.get_field(value).help_text,
                                 expected,
                                 "post.help_text с ошибкой.")

    def test_post_str_method(self):
        """Тест метода __str__(), модели Post"""
        value = TestModelGroup.group.__str__()
        expected = TestModelGroup.group.title
        self.assertEqual(value, expected, "__str__() не работает.")
