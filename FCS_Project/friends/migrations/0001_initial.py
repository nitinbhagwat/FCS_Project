# Generated by Django 2.2.4 on 2019-10-15 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sendername', models.CharField(default='', max_length=20)),
                ('recievername', models.CharField(default='', max_length=20)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'Friend',
                'unique_together': {('sendername', 'recievername')},
            },
        ),
    ]
