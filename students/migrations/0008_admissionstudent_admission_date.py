# Generated by Django 2.2.13 on 2020-10-10 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_auto_20201009_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='admissionstudent',
            name='admission_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
