# core/utils.py
from django.utils import timezone

def humanize_time_since(datetime_obj):
    """Retorna o tempo desde um datetime em formato legível."""
    now = timezone.now()
    diff = now - datetime_obj

    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60

    if days > 0:
        return f"{days} dia(s) atrás"
    if hours > 0:
        return f"{hours} hora(s) atrás"
    if minutes > 0:
        return f"{minutes} minuto(s) atrás"
    return "Agora mesmo"