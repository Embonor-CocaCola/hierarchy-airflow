from django.db import models

from customer.models import CustomerStaged
from expos.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime
from etl_job.models import EtlJob
from vendor.models import VendorStaged


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

    id = models.TextField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'airflow\".\"vendor_customer_conform'


class VendorCustomerStaged(models.Model):
    vendor_id = models.ForeignKey(VendorStaged, on_delete=models.CASCADE, db_column='vendor_id', db_constraint=False)
    customer_id = models.ForeignKey(
        CustomerStaged,
        on_delete=models.CASCADE,
        db_column='customer_id',
        db_constraint=False,
    )
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

    id = models.TextField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'airflow\".\"vendor_customer_staged'
