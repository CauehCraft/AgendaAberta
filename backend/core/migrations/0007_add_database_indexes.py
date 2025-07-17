from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_update_agendamento_fields'),
    ]

    operations = [
        # Adicionar índices para o modelo Horario
        migrations.AddIndex(
            model_name='horario',
            index=models.Index(fields=['dia_semana'], name='horario_dia_semana_idx'),
        ),
        migrations.AddIndex(
            model_name='horario',
            index=models.Index(fields=['hora_inicio'], name='horario_hora_inicio_idx'),
        ),
        migrations.AddIndex(
            model_name='horario',
            index=models.Index(fields=['hora_fim'], name='horario_hora_fim_idx'),
        ),
        migrations.AddIndex(
            model_name='horario',
            index=models.Index(fields=['local'], name='horario_local_idx'),
        ),
        migrations.AddIndex(
            model_name='horario',
            index=models.Index(fields=['ativo'], name='horario_ativo_idx'),
        ),
        migrations.AddIndex(
            model_name='horario',
            index=models.Index(fields=['ultima_atualizacao'], name='horario_ultima_atualizacao_idx'),
        ),
        
        # Adicionar índices para o modelo Disciplina
        migrations.AddIndex(
            model_name='disciplina',
            index=models.Index(fields=['nome'], name='disciplina_nome_idx'),
        ),
        migrations.AddIndex(
            model_name='disciplina',
            index=models.Index(fields=['curso'], name='disciplina_curso_idx'),
        ),
        migrations.AddIndex(
            model_name='disciplina',
            index=models.Index(fields=['semestre'], name='disciplina_semestre_idx'),
        ),
        migrations.AddIndex(
            model_name='disciplina',
            index=models.Index(fields=['ativo'], name='disciplina_ativo_idx'),
        ),
        
        # Adicionar índices para o modelo Agendamento
        migrations.AddIndex(
            model_name='agendamento',
            index=models.Index(fields=['data'], name='agendamento_data_idx'),
        ),
        migrations.AddIndex(
            model_name='agendamento',
            index=models.Index(fields=['status'], name='agendamento_status_idx'),
        ),
    ]