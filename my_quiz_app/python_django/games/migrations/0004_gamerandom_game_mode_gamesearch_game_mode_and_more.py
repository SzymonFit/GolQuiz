# Generated by Django 5.0.7 on 2024-07-29 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_gamerandom_answers_gamerandom_questions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamerandom',
            name='game_mode',
            field=models.CharField(default='default_mode', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gamesearch',
            name='game_mode',
            field=models.CharField(default='default_mode', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gamesolo',
            name='game_mode',
            field=models.CharField(default='mode1', max_length=20),
            preserve_default=False,
        ),
    ]