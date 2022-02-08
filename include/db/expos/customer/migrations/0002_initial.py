# Generated by Django 3.2.9 on 2022-02-07 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('etl_job', '0001_initial'),
        ('customer', '0001_initial'),
        ('plant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerstaged',
            name='plant_id',
            field=models.ForeignKey(db_column='plant_id', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='plant.plantstaged'),
        ),
        migrations.AddField(
            model_name='customerraw',
            name='job_id',
            field=models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob'),
        ),
        migrations.AddField(
            model_name='customerconform',
            name='job_id',
            field=models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob'),
        ),
    ]
