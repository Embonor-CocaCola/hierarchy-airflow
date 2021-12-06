from django.db import models
from gac.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime
from etl_job.models import EtlJob


class SupervisorPlantRaw(models.Model):
    supervisor_id = models.TextField(blank=True, null=True)
    supervisor_code = models.TextField(blank=True, null=True)
    supervisor_name = models.TextField(blank=True, null=True)
    supervisor_location = models.TextField(blank=True, null=True)
    chief_id = models.TextField(blank=True, null=True)
    plant_id = models.TextField(blank=True, null=True)
    role = models.TextField(blank=True, null=True)
    chief_unit = models.TextField(blank=True, null=True)

    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        managed = True
        db_table = 'airflow\".\"supervisor_plant_raw'


class SupervisorPlantTyped(models.Model):
    supervisor_id = models.IntegerField()
    supervisor_code = models.TextField(blank=True, null=True)
    supervisor_name = models.TextField()
    supervisor_location = models.TextField(blank=True, null=True)
    chief_id = models.IntegerField()
    plant_id = models.IntegerField()
    role = models.TextField(blank=True, null=True)
    chief_unit = models.TextField(blank=True, null=True)

    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        managed = True
        db_table = 'airflow\".\"supervisor_plant_typed'


class SupervisorConform(models.Model):
    source_id = models.IntegerField()
    code = models.TextField(blank=True, null=True)
    name = models.TextField()
    location = models.TextField(blank=True, null=True)
    chief_id = models.IntegerField()
    plant_id = models.IntegerField()
    role = models.TextField(blank=True, null=True)

    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        managed = True
        db_table = 'airflow\".\"supervisor_conform'
