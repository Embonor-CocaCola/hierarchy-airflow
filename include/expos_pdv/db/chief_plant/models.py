from django.db import models

from etl_job.models import ExposEtlJob
from expos.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime

from plant.models import PlantStaged


class ChiefPlantRaw(models.Model):
    chief_id = models.TextField(blank=True, null=True)
    chief_code = models.TextField(blank=True, null=True)
    chief_name = models.TextField(blank=True, null=True)
    chief_location = models.TextField(blank=True, null=True)
    chief_rut = models.TextField(blank=True, null=True)
    plant_id = models.TextField(blank=True, null=True)
    role = models.TextField(blank=True, null=True)
    chief_unit = models.TextField(blank=True, null=True)

    job_id = models.ForeignKey(
        ExposEtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'chief_plant'
        managed = True
        db_table = 'airflow\".\"chief_plant_raw'


class ChiefPlantTyped(models.Model):
    chief_id = models.IntegerField()
    chief_code = models.TextField(blank=True, null=True)
    chief_name = models.TextField()
    chief_location = models.TextField(blank=True, null=True)
    chief_rut = models.TextField()
    plant_id = models.IntegerField()
    role = models.TextField(blank=True, null=True)
    chief_unit = models.TextField(blank=True, null=True)

    job_id = models.ForeignKey(
        ExposEtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'chief_plant'
        managed = True
        db_table = 'airflow\".\"chief_plant_typed'


class ChiefConform(models.Model):
    source_id = models.IntegerField()
    code = models.TextField(blank=True, null=True)
    name = models.TextField()
    location = models.TextField(blank=True, null=True)
    rut = models.TextField()
    plant_id = models.IntegerField()
    role = models.TextField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)

    job_id = models.ForeignKey(
        ExposEtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = models.UUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'chief_plant'
        managed = True
        db_table = 'airflow\".\"chief_conform'


class ChiefStaged(models.Model):
    source_id = models.IntegerField()
    code = models.TextField(blank=True, null=True)
    name = models.TextField()
    location = models.TextField(blank=True, null=True)
    rut = models.TextField()
    plant_id = models.ForeignKey(PlantStaged, on_delete=models.CASCADE, db_column='plant_id', db_constraint=False)
    role = models.TextField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)

    job_id = models.ForeignKey(
        ExposEtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = models.UUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'chief_plant'
        managed = True
        db_table = 'airflow\".\"chief_staged'
