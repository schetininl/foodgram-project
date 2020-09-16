from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """Добавляет поле class к input формы"""
    return field.as_widget(attrs={"class": css})
