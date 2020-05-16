from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE

from common.models import BasicModel


class News(BasicModel):
    NEWS_STATUS_CHOICES = (
        ('IA', 'Неактивна'),
        ('A', 'Активна'),
    )

    title = models.CharField(max_length=512, verbose_name="Заглавие")
    tag = models.CharField(null=True, blank=True, max_length=512, verbose_name="Тег")
    author = models.ForeignKey(User, on_delete=CASCADE, related_name='news', verbose_name="Автор")
    news_status = models.CharField(max_length=2, choices=NEWS_STATUS_CHOICES, default='IA', verbose_name="Статус новости")
    content = RichTextField()

    class Meta:
        verbose_name = 'Нововсть'
        verbose_name_plural = 'Новости'


class Comment(BasicModel):
    news = models.ForeignKey(News, on_delete=CASCADE, related_name='comments', verbose_name="Новость")
    author = models.ForeignKey(User, on_delete=CASCADE, related_name='comments', verbose_name="Автор")
    content = models.TextField()


    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
