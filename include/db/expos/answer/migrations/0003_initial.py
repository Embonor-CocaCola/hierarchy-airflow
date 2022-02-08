# Generated by Django 3.2.9 on 2022-02-07 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('etl_job', '0001_initial'),
        ('question', '0001_initial'),
        ('vendor', '0001_initial'),
        ('answer', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='selfevaluationstaged',
            name='vendor_id',
            field=models.ForeignKey(db_column='vendor_id', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='vendor.vendorstaged'),
        ),
        migrations.AddField(
            model_name='selfevaluationfailedinserts',
            name='job_id',
            field=models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob'),
        ),
        migrations.AddField(
            model_name='selfevaluationconform',
            name='job_id',
            field=models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob'),
        ),
        migrations.AddField(
            model_name='answertyped',
            name='job_id',
            field=models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob'),
        ),
        migrations.AddField(
            model_name='answerstaged',
            name='job_id',
            field=models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob'),
        ),
        migrations.AddField(
            model_name='answerstaged',
            name='question_id',
            field=models.ForeignKey(db_column='question_id', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='question.questionstaged'),
        ),
        migrations.AddField(
            model_name='answerraw',
            name='job_id',
            field=models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob'),
        ),
        migrations.AddField(
            model_name='answerconform',
            name='job_id',
            field=models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob'),
        ),
    ]
