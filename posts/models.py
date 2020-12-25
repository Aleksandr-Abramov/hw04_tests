from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        verbose_name="Название группы:",
        max_length=200,
        help_text="Введите название группы"
    )
    slug = models.SlugField(
        verbose_name="Адрес в интернете:",
        unique=True,
        help_text=("Укажите адрес страницы, указывающий на группу. "
                   "Используйте латиницу, цифры, дефисы и знаки подчёркивания.")
    )
    description = models.TextField(
        verbose_name="Информация о авторе.",
        help_text="Справочная информация о авторе."
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name="Текст поста",
        help_text="Поле для хранения произвольного текста"
    )
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор поста:",
        help_text="Пользователь опубликовавший пост."
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name="posts",
        blank=True,
        null=True,
        verbose_name="Автор:",
        help_text="Автор."
    )

    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text[:15]
