from datetime import datetime
from django.db import models

from include.expos_pdv.db.expos.models import DateTimeWithoutTZField


class EtlJob(models.Model):
    dag_run_id = models.CharField(max_length=255)
    attempt = models.IntegerField(default=0)
    created_at = DateTimeWithoutTZField(default=datetime.now, editable=False)

    class Meta:
        managed = True
        db_table = 'airflow\".\"etl_job'
        constraints = [
            models.UniqueConstraint(
                fields=['dag_run_id', 'attempt'],
                name='etljob_airflow_uidx',
            ),
        ]
