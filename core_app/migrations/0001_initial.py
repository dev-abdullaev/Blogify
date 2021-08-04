# Generated by Django 3.2.5 on 2021-08-04 10:58

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('body', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('published', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to='pictures/')),
                ('snippet', models.CharField(default='Click read more button to read...', max_length=250)),
            ],
            options={
                'ordering': ['-created', '-published'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('username', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
                ('bio', models.TextField(blank=True, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('facebook_url', models.CharField(blank=True, max_length=550, null=True)),
                ('instagram_url', models.CharField(blank=True, max_length=550, null=True)),
                ('twitter_url', models.CharField(blank=True, max_length=550, null=True)),
            ],
        ),
    ]