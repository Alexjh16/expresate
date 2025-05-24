from django import template

register = template.Library()

@register.filter
def duracion_legible(segundos):
    try:
        segundos = int(segundos)
        minutos = segundos // 60
        seg = segundos % 60
        return f"{minutos:02}:{seg:02}"
    except:
        return "--:--"