# Generated by Django 4.2.7 on 2023-11-14 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_summary_input_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='summary',
            name='owner',
        ),
    ]