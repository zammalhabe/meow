# Generated by Django 2.0.4 on 2019-06-06 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0007_smpost_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posthistory',
            old_name='post_instagram',
            new_name='post_twitter',
        ),
    ]
