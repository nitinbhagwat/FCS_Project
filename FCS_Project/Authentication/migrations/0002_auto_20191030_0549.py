# Generated by Django 2.2.4 on 2019-10-30 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='uTimelinePrivacy',
            field=models.CharField(choices=[('only me', 'Only Me'), ('friends', 'Friends'), ('global', 'Global')], default='global', max_length=20),
        ),
    ]