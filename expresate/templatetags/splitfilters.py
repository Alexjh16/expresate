from django import template

register = template.Library()

@register.filter
def split_before(value, sep='-'):
    return value.split(sep, 1)[0].strip()

@register.filter
def split_after(value, sep='-'):
    return value.split(sep, 1)[1].strip() if sep in value else ''

@register.filter
def index(List, i):
    try:
        return List[int(i)]
    except:
        return ''