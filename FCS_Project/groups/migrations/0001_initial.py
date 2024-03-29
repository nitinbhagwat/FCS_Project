# Generated by Django 2.2.6 on 2019-10-30 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Joined_group',
            fields=[
                ('firstfield', models.CharField(default='', max_length=50, primary_key=True, serialize=False)),
                ('group_name', models.CharField(default='', max_length=20)),
                ('member_name', models.CharField(default='', max_length=20)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'joined_Group',
                'unique_together': {('group_name', 'member_name')},
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_name', models.CharField(default='', max_length=20, primary_key=True, serialize=False)),
                ('admin_name', models.CharField(default='', max_length=20)),
                ('price', models.IntegerField(default=0)),
                ('type', models.IntegerField(default='')),
            ],
            options={
                'db_table': 'Group',
                'unique_together': {('group_name', 'admin_name')},
            },
        ),
    ]
