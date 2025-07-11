from django.contrib import admin
from .models import Agendamento, CustomUser, Disciplina, Horario

admin.site.register(CustomUser)
admin.site.register(Disciplina)
admin.site.register(Horario)
admin.site.register(Agendamento)