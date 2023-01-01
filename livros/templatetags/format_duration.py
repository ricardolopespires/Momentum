from django import template

register = template.Library()

@register.filter
def duration(td):
    segundos = int(td.total_seconds())
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60

    return '0{} h:{} min:{} seg'.format(horas, minutos, segundos)





