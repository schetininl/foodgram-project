from django import template

register = template.Library()


@register.filter
def countCalc(field):
    #result = int(field) - 3
    result = str(int(field) - 3)
    if result[-1:] == '1':
        return result+' рецепт...'
    elif result[-1:] in ['2', '3', '4']:
        return result+' рецепта...'
    else:
        return result+' рецептов...'
    return str(result)[-1:]
