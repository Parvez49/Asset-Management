# Generated by Django 4.2 on 2023-08-10 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_alter_user_options_alter_user_managers_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="User",
            new_name="UserData",
        ),
    ]
