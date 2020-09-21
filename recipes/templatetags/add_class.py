from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """Добавляет поле class к input формы"""
    return field.as_widget(attrs={"class": css})


@register.filter
def class_tag(tag):
    """Возвращает необходимое поле class
    для кнопки включения/выключения тега"""
    classes = {
        "breakfast": "badge badge_style_orange",
        "lunch": "badge badge_style_green",
        "dinner": "badge badge_style_purple",
    }
    return classes[tag]
