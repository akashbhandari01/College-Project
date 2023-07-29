# Generated by Django 4.2 on 2023-04-17 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iamge', models.ImageField(null=True, upload_to='')),
                ('title', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('slug', models.SlugField(default=' ', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ManyToManyField(blank=True, to='app.user')),
            ],
        ),
    ]
