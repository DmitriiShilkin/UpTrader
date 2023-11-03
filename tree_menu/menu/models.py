from django.db import models


class Menu(models.Model):
    title = models.CharField('Название меню', max_length=128, unique=True)
    slug = models.SlugField('Slug для меню', max_length=128)

    def __str__(self):
        return self.title.capitalize()


class Item(models.Model):
    title = models.CharField('Название пункта меню', max_length=128)
    slug = models.SlugField('Slug для пункта меню', max_length=128)
    menu = models.ForeignKey(Menu, blank=True, null=True, related_name='items', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title.capitalize()

