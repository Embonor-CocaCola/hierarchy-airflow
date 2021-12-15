from django.db import models

from branch_office.models import BranchOfficeStaged
from gac.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime
from etl_job.models import EtlJob
from plant.models import PlantStaged


class CustomerRaw(models.Model):
    source_id = models.TextField(blank=True, null=True)
    price_list = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    dni = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    street = models.TextField(blank=True, null=True)
    street_number = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    sub_location = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null=True)
    branch_office = models.TextField(blank=True, null=True)
    business_name = models.TextField(blank=True, null=True)
    category_name = models.TextField(blank=True, null=True)
    category_id = models.TextField(blank=True, null=True)
    main_category_name = models.TextField(blank=True, null=True)
    main_category_id = models.TextField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    credit_amount = models.TextField(blank=True, null=True)
    credit_balance = models.TextField(blank=True, null=True)
    duty_free_price_list = models.TextField(blank=True, null=True)
    plant_id = models.TextField(blank=True, null=True)
    zone_id = models.TextField(blank=True, null=True)
    route_id = models.TextField(blank=True, null=True)
    territory_id = models.TextField(blank=True, null=True)
    channel_mkt = models.TextField(blank=True, null=True)
    country_specific = models.TextField(blank=True, null=True)
    geog = models.TextField(blank=True, null=True)
    deleted_at = models.TextField(blank=True, null=True)
    market_group_id = models.TextField(blank=True, null=True)
    market_chain_id = models.TextField(blank=True, null=True)

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
        db_table = 'airflow\".\"customer_raw'


class CustomerTyped(models.Model):
    source_id = models.IntegerField()
    price_list = models.IntegerField()
    name = models.TextField()
    dni = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    street = models.TextField(blank=True, null=True)
    street_number = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    sub_location = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null=True)
    branch_office = models.IntegerField()
    business_name = models.TextField(blank=True, null=True)
    category_name = models.TextField(blank=True, null=True)
    category_id = models.TextField(blank=True, null=True)
    main_category_name = models.TextField(blank=True, null=True)
    main_category_id = models.TextField(blank=True, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    observations = models.TextField(blank=True, null=True)
    credit_amount = models.IntegerField(null=True)
    credit_balance = models.IntegerField(null=True)
    duty_free_price_list = models.IntegerField(null=True)
    plant_id = models.IntegerField()
    zone_id = models.IntegerField()
    route_id = models.IntegerField()
    territory_id = models.IntegerField()
    channel_mkt = models.TextField(blank=True, null=True)
    country_specific = models.JSONField()
    deleted_at = models.DateField(null=True)
    market_group_id = models.TextField(blank=True, null=True)
    market_chain_id = models.TextField(blank=True, null=True)

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
        db_table = 'airflow\".\"customer_typed'


class CustomerConform(models.Model):
    source_id = models.IntegerField()
    price_list = models.IntegerField()
    name = models.TextField()
    dni = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    street = models.TextField(blank=True, null=True)
    street_number = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    sub_location = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null=True)
    branch_office = models.IntegerField()
    business_name = models.TextField(blank=True, null=True)
    category_name = models.TextField(blank=True, null=True)
    category_id = models.TextField(blank=True, null=True)
    main_category_name = models.TextField(blank=True, null=True)
    main_category_id = models.TextField(blank=True, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    observations = models.TextField(blank=True, null=True)
    credit_amount = models.IntegerField(null=True)
    credit_balance = models.IntegerField(null=True)
    duty_free_price_list = models.IntegerField(null=True)
    plant_id = models.IntegerField()
    zone_id = models.IntegerField()
    route_id = models.IntegerField()
    territory_id = models.IntegerField()
    channel_mkt = models.TextField(blank=True, null=True)
    cluster = models.TextField(null=True)
    deleted_at = models.DateField(null=True)
    market_group_id = models.TextField(blank=True, null=True)
    market_chain_id = models.TextField(blank=True, null=True)

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
        db_table = 'airflow\".\"customer_conform'


class CustomerStaged(models.Model):
    source_id = models.IntegerField()
    price_list = models.IntegerField()
    name = models.TextField()
    dni = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    street = models.TextField(blank=True, null=True)
    street_number = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    sub_location = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null=True)
    branch_office_id = models.ForeignKey(
        BranchOfficeStaged,
        on_delete=models.CASCADE,
        db_column='branch_office_id',
        db_constraint=False,
    )
    business_name = models.TextField(blank=True, null=True)
    category_name = models.TextField(blank=True, null=True)
    category_id = models.TextField(blank=True, null=True)
    main_category_name = models.TextField(blank=True, null=True)
    main_category_id = models.TextField(blank=True, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    observations = models.TextField(blank=True, null=True)
    credit_amount = models.IntegerField(null=True)
    credit_balance = models.IntegerField(null=True)
    duty_free_price_list = models.IntegerField(null=True)
    plant_id = models.ForeignKey(PlantStaged, on_delete=models.CASCADE, db_column='plant_id', db_constraint=False)
    zone_id = models.IntegerField()
    route_id = models.IntegerField()
    territory_id = models.IntegerField()
    channel_mkt = models.TextField(blank=True, null=True)
    cluster = models.TextField(null=True)
    deleted_at = models.DateField(null=True)
    market_group_id = models.TextField(blank=True, null=True)
    market_chain_id = models.TextField(blank=True, null=True)

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
        db_table = 'airflow\".\"customer_staged'
