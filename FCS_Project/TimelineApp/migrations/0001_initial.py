# Generated by Django 2.2.6 on 2019-10-30 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user_name', models.CharField(max_length=10)),
                ('to_user_name', models.CharField(max_length=10)),
                ('posted_message', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('from_user_gender', models.BooleanField(default=True)),
            ],
        ),
    ]
