# Generated by Django 3.1.2 on 2020-10-14 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='questionset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('question', models.TextField(max_length=100)),
                ('priority', models.CharField(choices=[('L', 'low'), ('M', 'medium'), ('H', 'high')], max_length=1)),
            ],
            options={
                'verbose_name': 'people question',
                'verbose_name_plural': 'FAQ',
            },
        ),
    ]
