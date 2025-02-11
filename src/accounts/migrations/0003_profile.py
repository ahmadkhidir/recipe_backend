# Generated by Django 5.0.3 on 2024-05-02 12:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_id'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='profiles/', verbose_name='Image')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='profiles/', verbose_name='Cover Image')),
                ('dislikes', models.ManyToManyField(blank=True, related_name='disliked_users', to='recipes.cuisine')),
                ('interests', models.ManyToManyField(blank=True, related_name='interested_users', to='recipes.cuisine')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
