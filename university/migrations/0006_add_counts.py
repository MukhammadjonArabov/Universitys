# Generated manually: add counts to University
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('university', '0005_remove_employee_degree_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='faculties_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='university',
            name='directions_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='university',
            name='students_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
