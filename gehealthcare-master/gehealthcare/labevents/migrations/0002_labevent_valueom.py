# Generated by Django 2.1.2 on 2018-12-10 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labevents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='labevent',
            name='valueom',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]