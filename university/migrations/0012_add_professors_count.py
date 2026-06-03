# Generated manually: add professors_count to University
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('university', '0011_merge_counts_and_socialapps'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='professors_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
