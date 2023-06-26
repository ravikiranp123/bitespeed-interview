# Generated by Django 4.2.2 on 2023-06-25 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNumber', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=45)),
                ('linkPrecedence', models.CharField(choices=[('primary', 'Primary'), ('secondary', 'Secondary')], max_length=30)),
                ('createdAt', models.DateTimeField()),
                ('updatedAt', models.DateTimeField()),
                ('deletedAt', models.DateTimeField()),
                ('linkedId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='identity_reconciliation.user')),
            ],
        ),
    ]
