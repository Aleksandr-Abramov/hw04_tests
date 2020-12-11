from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views

urlpatterns = [
    #  регистрация и авторизация
    path("auth/", include("users.urls")),
    path("about/", include("django.contrib.flatpages.urls")),

    #  если нужного шаблона для /auth не нашлось в файле users.urls —
    #  ищем совпадения в файле django.contrib.auth.urls
    path('auth/', include('users.urls')),
    path("auth/", include("django.contrib.auth.urls")),

    #  раздел администратора
    path("admin/", admin.site.urls),

    #  обработчик для главной страницы ищем в urls.py приложения posts
    path('about-us/', views.flatpage, {'url': '/about-author/'}, name='about'),
    path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),
    path("", include("posts.urls")),
]
