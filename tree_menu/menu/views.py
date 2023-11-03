from django.shortcuts import render

from .models import Menu


# Представление для стартовой страницы
def index_view(request):
    menu = Menu.objects.filter(slug='main_menu').first()
    context = {
        'menu': menu
    }

    return render(request, "index.html", context)

