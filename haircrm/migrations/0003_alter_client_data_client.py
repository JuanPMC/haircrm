# Generated by Django 4.2.4 on 2023-09-15 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('haircrm', '0002_client_client_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client_data',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='userData', to='haircrm.client'),
        ),
    ]
