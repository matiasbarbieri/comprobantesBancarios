# Generated by Django 4.2.1 on 2023-05-28 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comprobante',
            options={'ordering': ['-fecha_subida']},
        ),
        migrations.RenameField(
            model_name='comprobante',
            old_name='fehca_subida',
            new_name='fecha_subida',
        ),
    ]
