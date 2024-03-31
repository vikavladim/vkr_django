from django import template

from schedule.views import menus

register = template.Library()


@register.inclusion_tag('menus.html')
def get_menu(menu_selected=menus[0]['url']):
    return {'menu_selected': menu_selected, 'menus': menus}
