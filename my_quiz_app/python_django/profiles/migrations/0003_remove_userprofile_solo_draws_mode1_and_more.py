# Generated by Django 5.0.7 on 2024-08-06 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_rename_draws_userprofile_pvp_draws_mode1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='solo_draws_mode1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='solo_draws_mode2',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='solo_draws_mode3',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='solo_losses_mode1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='solo_losses_mode2',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='solo_losses_mode3',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='solo_wins_mode1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='solo_wins_mode2',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='solo_wins_mode3',
        ),
    ]
