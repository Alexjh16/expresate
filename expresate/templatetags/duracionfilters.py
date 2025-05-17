from django import template

register = template.Library()

@register.filter
def duracion_legible(segundos):
    try:
        segundos = int(segundos)
    except (ValueError, TypeError):
        return ""
    if segundos < 60:
        return f"{segundos} seg"
    minutos = segundos // 60
    horas = minutos // 60
    minutos = minutos % 60
    if horas > 0:
        if minutos > 0:
            return f"{horas}h {minutos}m"
        return f"{horas}h"
    return f"{minutos} min"