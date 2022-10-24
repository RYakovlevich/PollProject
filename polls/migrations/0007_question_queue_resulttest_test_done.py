# Generated by Django 4.1.2 on 2022-10-24 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_alter_choice_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='queue',
            field=models.IntegerField(default=1, verbose_name='Очередность'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resulttest',
            name='test_done',
            field=models.BooleanField(default=False),
        ),
    ]
