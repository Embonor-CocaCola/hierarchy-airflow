from django.db import models
from gac.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime
from etl_job.models import EtlJob


class VendorCustomerRaw(models.Model):
    vendor_id = models.TextField(blank=True, null=True)
    customer_id = models.TextField(blank=True, null=True)
    start_date = models.TextField(blank=True, null=True)
    frequency = models.TextField(blank=True, null=True)
    priority = models.TextField(blank=True, null=True)

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
        db_table = 'airflow\".\"vendor_customer_raw'


class VendorCustomerTyped(models.Model):
    vendor_id = models.IntegerField()
    customer_id = models.IntegerField()
    start_date = models.DateField()
    frequency = models.IntegerField()
    priority = models.IntegerField()

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
        db_table = 'airflow\".\"vendor_customer_typed'


class VendorCustomerConform(models.Model):
    vendor_id = models.IntegerField()
    customer_id = models.IntegerField()
    start_date = models.DateField()
    frequency = models.IntegerField()
    priority = models.IntegerField()

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
        db_table = 'airflow\".\"vendor_customer_conform'
