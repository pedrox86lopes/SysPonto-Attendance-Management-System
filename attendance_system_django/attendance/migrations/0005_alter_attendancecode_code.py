# Generated by Django 5.2 on 2025-06-16 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_attendancecode_generated_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancecode',
            name='code',
            field=models.CharField(blank=True, default='DUMMY0', max_length=6, unique=True),
            preserve_default=False,
        ),
    ]
