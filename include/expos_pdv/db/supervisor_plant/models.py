from django.db import models

from include.expos_pdv import ChiefStaged
from include.expos_pdv.db.expos.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime
from include.expos_pdv import EtlJob
from include.expos_pdv import PlantStaged


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


class SupervisorStaged(models.Model):
    source_id = models.IntegerField()
    code = models.TextField(blank=True, null=True)
    name = models.TextField()
    location = models.TextField(blank=True, null=True)
    chief_id = models.ForeignKey(ChiefStaged, on_delete=models.CASCADE, db_column='chief_id', db_constraint=False)
    plant_id = models.ForeignKey(PlantStaged, on_delete=models.CASCADE, db_column='plant_id', db_constraint=False)
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
        db_table = 'airflow\".\"supervisor_staged'
