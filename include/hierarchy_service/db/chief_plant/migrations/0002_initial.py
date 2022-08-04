# Generated by Django 3.2.9 on 2022-07-20 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('etl_job', '0001_initial'),
        ('chief_plant', '0001_initial'),
        ('plant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chiefstaged',
            name='plant_id',
            field=models.ForeignKey(db_column='plant_id', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='plant.plantstaged'),
        ),
        migrations.AddField(
            model_name='chiefplanttyped',
            name='job_id',
            field=models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob'),
        ),
        migrations.AddField(
            model_name='chiefplantraw',
            name='job_id',
            field=models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob'),
        ),
        migrations.AddField(
            model_name='chiefconform',
            name='job_id',
            field=models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob'),
        ),
    ]