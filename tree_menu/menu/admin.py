from django.contrib import admin

from .models import Menu, Item


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):

    list_display = ('title', 'slug')
    search_fields = ('title', 'slug')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = ('pk', 'title', 'parent')
    list_filter = ('menu',)
    search_fields = ('title', 'slug')
    ordering = ('pk',)

    # fieldsets = (
    #     ('Добавить новый пункт меню', {
    #         'description': "Parent should be a menu or item",
    #         'fields': (('menu', 'parent'), 'title', 'slug')
    #         }),
    # )
