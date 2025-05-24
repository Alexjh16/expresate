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
    segundos_restantes = segundos % 60
    minutos = minutos % 60
    if horas > 0:
        if minutos > 0 or segundos_restantes > 0:
            return f"{horas}h {minutos}m {segundos_restantes}s"
        return f"{horas}h"
    if minutos > 0:
        if segundos_restantes > 0:
            return f"{minutos} min {segundos_restantes} seg"
        return f"{minutos} min"
    return f"{segundos_restantes} seg"