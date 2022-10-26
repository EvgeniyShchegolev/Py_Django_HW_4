from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)
    tags = models.ManyToManyField(Tag, through='Scope')

    class Meta:
        ordering = ['published_at', ]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Scope(models.Model):
    is_main = models.BooleanField()
    tag = models.ForeignKey(Tag, related_name='scopes', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='scopes', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-is_main', 'tag', ]

    def __str__(self):
        return f'{self.is_main}'
