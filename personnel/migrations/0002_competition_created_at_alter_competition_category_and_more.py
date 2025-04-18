# Generated by Django 4.2.19 on 2025-03-29 14:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import personnel.models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='competition',
            name='category',
            field=models.CharField(choices=[('NLWL Winter League', 'NLWL Winter League'), ('Fintan Goss Cup', 'Fintan Goss Cup'), ('Summer League', 'Summer League'), ('Cup', 'Cup'), ('Friendly', 'Friendly'), ('Tournament', 'Tournament')], max_length=120),
        ),
        migrations.AlterField(
            model_name='competition',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(2006), personnel.models.max_value_current_year]),
        ),
        migrations.AlterField(
            model_name='match',
            name='competition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='personnel.competition'),
        ),
    ]
