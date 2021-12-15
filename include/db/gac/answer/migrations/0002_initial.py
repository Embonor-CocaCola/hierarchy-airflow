# Generated by Django 3.2.9 on 2021-12-14 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('answer', '0001_initial'),
        ('etl_job', '0004_create_find_question_id_from_portals_procedure'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='selfevaluationstaged',
            name='customer_id',
            field=models.ForeignKey(db_column='customer_id', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='customer.customerstaged'),
        ),
        migrations.AddField(
            model_name='selfevaluationstaged',
            name='job_id',
            field=models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob'),
        ),
    ]
