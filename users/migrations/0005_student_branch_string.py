# Generated by Django 3.2.5 on 2021-08-16 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_student_student_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='branch_string',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Branch'),
        ),
    ]
