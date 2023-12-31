# Generated by Django 4.1.10 on 2023-07-31 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminboundarymanager', '0003_alter_adminboundarysettings_data_source'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Countries',
            new_name='Country',
        ),
        migrations.AddField(
            model_name='adminboundarysettings',
            name='countries_must_share_boundaries',
            field=models.BooleanField(default=True, help_text='Validation to ensure that the selected countries share boundaries with each other. Used if two or more countries are set.', verbose_name='Countries must share boundaries - If more than one'),
        ),
    ]
