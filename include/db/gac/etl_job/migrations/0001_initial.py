import os

import datetime
from django.db import (
    migrations,
    models,
)
import gac.models


def get_raw_sql(filename):
    sql_path = os.path.join(os.path.dirname(__file__), 'sql', filename)
    return open(sql_path, 'r').read()


def create_slugify(): return get_raw_sql('0001_create_slugify.sql')
def drop_slugify(): return get_raw_sql('0002_drop_slugify.sql')


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EtlJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dag_run_id', models.CharField(max_length=255)),
                ('attempt', models.IntegerField(default=0)),
                ('created_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now, editable=False)),
            ],
            options={
                'db_table': 'airflow"."etl_job',
                'managed': True,
            },
        ),
        migrations.AddConstraint(
            model_name='etljob',
            constraint=models.UniqueConstraint(fields=('dag_run_id', 'attempt'), name='etljob_airflow_uidx'),
        ),
        migrations.RunSQL(create_slugify(), drop_slugify()),
    ]
