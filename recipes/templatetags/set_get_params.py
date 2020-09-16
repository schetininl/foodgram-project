from django import template

register = template.Library()


@register.simple_tag
def set_tags(request, tags, value):
    """Устанавливает get параметры в зависимости
    от выбранных тегов"""
    dict_ = request.GET.copy()
    #Если есть такой параметр в Get-запросе, то удаляем его
    if request.GET.get(value):
        del dict_[value]
    #Если такого параметра нет, но есть в переменной tags
    elif value in tags:
        for tag in tags:
            #Устанавливаем остальные теги(кроме выбранного)
            if tag != value:
                dict_[tag] = "tag"
    #Иначе мы добавляем этот параметр
    else:
        dict_[value] = "tag"

    return dict_.urlencode()


@register.simple_tag
def set_page(request, value):
    dict_ = request.GET.copy()
    dict_["page"] = value
    return dict_.urlencode()
