from django.db import models
from expos.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime
from etl_job.models import EtlJob
from plant.models import PlantStaged


class BranchOfficeRaw(models.Model):
    source_id = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )
    plant_id = models.TextField(blank=True, null=True)
    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        managed = True
        db_table = 'airflow\".\"branch_office_raw'


class BranchOfficeTyped(models.Model):
    source_id = models.IntegerField()
    name = models.TextField()
    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )
    plant_id = models.IntegerField()
    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'airflow\".\"branch_office_typed'


class BranchOfficeConform(models.Model):
    source_id = models.IntegerField()
    name = models.TextField()
    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )
    plant_id = models.IntegerField()
    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'airflow\".\"branch_office_conform'


class BranchOfficeStaged(models.Model):
    source_id = models.IntegerField()
    name = models.TextField()
    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )
    plant_id = models.ForeignKey(PlantStaged, on_delete=models.CASCADE, db_column='plant_id', db_constraint=False)
    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'airflow\".\"branch_office_staged'
