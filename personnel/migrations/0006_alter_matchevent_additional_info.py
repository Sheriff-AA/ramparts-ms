# Generated by Django 4.2.19 on 2025-04-01 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0005_alter_player_options_alter_player_position_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchevent',
            name='additional_info',
            field=models.CharField(blank=True, default=dict, max_length=250),
        ),
    ]
