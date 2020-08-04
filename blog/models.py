from django.db import models

from django.urls import reverse
from django.utils.text import slugify
from time import time
'''
1) Создание модели допустимо различными способами 
    1)  
    
    p = Post(title='New post', slug='new-slug', body='some text')
    p.save()
    
    2)
    
    p = Post.objects.create(title='New post', slug='new-slug', body='some text')

2) objects attr является менеджером модели, содержит набор методов для управления

3) метод objects.get()

    осуществляет поиск экземпляра модели по идентифицирующим параметрам. По дефолту метод чувствителен к регистру
    
    для сужения запроса поиска используется фича lookups
    
    post = Post.objects.get(slug="my-slug")             -> тут чувствителен к регистру
    post = Post.objects.get(slug__iexact="my-slug")     -> тут нет
    
    __iexact    - insensitive exact (нечувствительный к регистру)
    __contains  - проверка на наличие подстроки в строке. Для метода get может зарайзить ошибку если найдено более одного результата




'''


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return f"{new_slug}-{int(time())}"


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)  # index true by default because of unique
    body = models.TextField(blank=True, db_index=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    # связываем с моделью тэг, позволяем быть пустым, объявляем название поля для связанной модели
    # (без указания явным способом будет сгенерировано поле post_set)
    tags = models.ManyToManyField('Tag', blank=True, related_name="posts")

    class Meta:
        ordering = ["-date_pub"]

    def get_absolute_url(self):
        '''
        метод возвращает ссылку для доступа к экземпляру. из урлов тянем шаблон по имени и передаем ему кваргами
        параметры (url динамический)
        '''

        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """
        метод генерит слаг при создании нового поста. наличие id сообщает нам, что такой пост уже существует
        :param args:
        :param kwargs:
        :return:
        """
        if not self.id:
            self.slug = gen_slug(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]


























