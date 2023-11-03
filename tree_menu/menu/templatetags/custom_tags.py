from django import template
from django.core.exceptions import ObjectDoesNotExist

from ..models import Item

register = template.Library()


def get_sel_item_id_list(parent, root_item, sel_item_id):
    """
    Возвращает список всех ID для элементов выбранного меню, начиная с родительского элемента и до текущего.

    parent: родительский элемент меню.
    root_item: список элементов корневого меню.
    sel_item_id: ID элемента выбранного меню.
    """
    sel_item_id_list = []

    while parent:
        sel_item_id_list.append(parent.id)
        parent = parent.parent
    if not sel_item_id_list:
        for item in root_item:
            if item.id == sel_item_id:
                sel_item_id_list.append(sel_item_id)
    return sel_item_id_list


def get_child_items(items_values, cur_item_id, sel_item_id_list):
    """
    Возвращает список дочерних элементов для текущего элемента меню с ID.

    items_values: Список всех элементов меню.
    cur_item_id: ID элемента меню, для которого нужно получить дочерние элементы.
    sel_item_id_list: Список всех ID для элементов выбранного меню.
    """

    item_list = [item for item in items_values.filter(parent_id=cur_item_id)]
    for item in item_list:
        if item['id'] in sel_item_id_list:
            item['child_items'] = get_child_items(items_values, item['id'], sel_item_id_list)
    return item_list


def build_qs(context, menu):
    """
    Создает строку-запрос на основе текущего контекстного запроса.

    context: текущий контекст.
    menu: название меню.
    Возвращает строку-запрос.
    """

    # Инициализация списка для хранения аргументов строки-запроса
    qs_args = []

    # Цикл по всем параметрам текущего запроса
    for key in context['request'].GET:
        # Если ключ текущего параметра не соответствует параметру 'menu'
        if key != menu:
            # Добавляем пару ключ-значение в список аргументов строки-запроса
            qs_args.append(f"{key}={context['request'].GET[key]}")

    # Объединяем все аргументы списка в одну строку-запрос с разделителем '&'
    querystring = '&'.join(qs_args)

    # Возвращаем строку-запрос
    return querystring


@register.inclusion_tag('tmenu.html', takes_context=True)
def draw_menu(context, menu):
    """
    Пользовательский template tag для отрисовки древовидного меню.

    context: данные контекста из представления.
    menu: название меню.
    Возвращает словарь, данные из которого будут использованы для отображения древовидного меню согласно шаблону
    tmenu.html.
    """

    try:
        # Получаем все элементы текущего меню
        items = Item.objects.filter(menu__title=menu)
        items_values = items.values()

        # Получаем элементы корневого меню (у которого нет родителя)
        root_item = [item for item in items_values.filter(parent=None)]

        # Определяем ID выбранного элемента меню из параметров запроса
        sel_item_id = int(context['request'].GET[menu])
        sel_item = items.get(id=sel_item_id)

        # Получаем список всех ID для элементов выбранного меню
        sel_item_id_list = get_sel_item_id_list(sel_item, root_item, sel_item_id)

        # Добавляем потомков для каждого выбранного элемента меню
        for item in root_item:
            if item['id'] in sel_item_id_list:
                item['child_items'] = get_child_items(items_values, item['id'], sel_item_id_list)

        result_dict = {'items': root_item}

    except (KeyError, ObjectDoesNotExist):
        # В случае ошибки, возвращаем список элементов меню без родительских элементов
        result_dict = {
            'items': [
                item for item in Item.objects.filter(menu__title=menu, parent=None).values()
            ]
        }

    # Добавляем название меню и дополнительную строку-запрос к результирующему словарю
    result_dict['menu'] = menu
    result_dict['other_qs'] = build_qs(context, menu)

    return result_dict


