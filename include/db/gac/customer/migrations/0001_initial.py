# Generated by Django 3.2.9 on 2021-12-09 13:23

import datetime
from django.db import migrations, models
import django.db.models.deletion
import gac.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('etl_job', '0004_create_find_question_id_from_portals_procedure'),
        ('branch_office', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerConform',
            fields=[
                ('source_id', models.IntegerField()),
                ('price_list', models.IntegerField()),
                ('name', models.TextField()),
                ('dni', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('street', models.TextField(blank=True, null=True)),
                ('street_number', models.TextField(blank=True, null=True)),
                ('location', models.TextField(blank=True, null=True)),
                ('sub_location', models.TextField(blank=True, null=True)),
                ('phone_number', models.TextField(blank=True, null=True)),
                ('branch_office', models.IntegerField()),
                ('business_name', models.TextField(blank=True, null=True)),
                ('category_name', models.TextField(blank=True, null=True)),
                ('category_id', models.TextField(blank=True, null=True)),
                ('main_category_name', models.TextField(blank=True, null=True)),
                ('main_category_id', models.TextField(blank=True, null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('observations', models.TextField(blank=True, null=True)),
                ('credit_amount', models.IntegerField(null=True)),
                ('credit_balance', models.IntegerField(null=True)),
                ('duty_free_price_list', models.IntegerField(null=True)),
                ('plant_id', models.IntegerField()),
                ('zone_id', models.IntegerField()),
                ('route_id', models.IntegerField()),
                ('territory_id', models.IntegerField()),
                ('channel_mkt', models.TextField(blank=True, null=True)),
                ('country_specific', models.JSONField()),
                ('deleted_at', models.DateField(null=True)),
                ('market_group_id', models.TextField(blank=True, null=True)),
                ('market_chain_id', models.TextField(blank=True, null=True)),
                ('created_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', gac.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'airflow"."customer_conform',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CustomerRaw',
            fields=[
                ('source_id', models.TextField(blank=True, null=True)),
                ('price_list', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('dni', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('street', models.TextField(blank=True, null=True)),
                ('street_number', models.TextField(blank=True, null=True)),
                ('location', models.TextField(blank=True, null=True)),
                ('sub_location', models.TextField(blank=True, null=True)),
                ('phone_number', models.TextField(blank=True, null=True)),
                ('branch_office', models.TextField(blank=True, null=True)),
                ('business_name', models.TextField(blank=True, null=True)),
                ('category_name', models.TextField(blank=True, null=True)),
                ('category_id', models.TextField(blank=True, null=True)),
                ('main_category_name', models.TextField(blank=True, null=True)),
                ('main_category_id', models.TextField(blank=True, null=True)),
                ('latitude', models.TextField(blank=True, null=True)),
                ('longitude', models.TextField(blank=True, null=True)),
                ('observations', models.TextField(blank=True, null=True)),
                ('credit_amount', models.TextField(blank=True, null=True)),
                ('credit_balance', models.TextField(blank=True, null=True)),
                ('duty_free_price_list', models.TextField(blank=True, null=True)),
                ('plant_id', models.TextField(blank=True, null=True)),
                ('zone_id', models.TextField(blank=True, null=True)),
                ('route_id', models.TextField(blank=True, null=True)),
                ('territory_id', models.TextField(blank=True, null=True)),
                ('channel_mkt', models.TextField(blank=True, null=True)),
                ('country_specific', models.TextField(blank=True, null=True)),
                ('geog', models.TextField(blank=True, null=True)),
                ('deleted_at', models.TextField(blank=True, null=True)),
                ('market_group_id', models.TextField(blank=True, null=True)),
                ('market_chain_id', models.TextField(blank=True, null=True)),
                ('created_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', gac.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'airflow"."customer_raw',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CustomerTyped',
            fields=[
                ('source_id', models.IntegerField()),
                ('price_list', models.IntegerField()),
                ('name', models.TextField()),
                ('dni', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('street', models.TextField(blank=True, null=True)),
                ('street_number', models.TextField(blank=True, null=True)),
                ('location', models.TextField(blank=True, null=True)),
                ('sub_location', models.TextField(blank=True, null=True)),
                ('phone_number', models.TextField(blank=True, null=True)),
                ('branch_office', models.IntegerField()),
                ('business_name', models.TextField(blank=True, null=True)),
                ('category_name', models.TextField(blank=True, null=True)),
                ('category_id', models.TextField(blank=True, null=True)),
                ('main_category_name', models.TextField(blank=True, null=True)),
                ('main_category_id', models.TextField(blank=True, null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('observations', models.TextField(blank=True, null=True)),
                ('credit_amount', models.IntegerField(null=True)),
                ('credit_balance', models.IntegerField(null=True)),
                ('duty_free_price_list', models.IntegerField(null=True)),
                ('plant_id', models.IntegerField()),
                ('zone_id', models.IntegerField()),
                ('route_id', models.IntegerField()),
                ('territory_id', models.IntegerField()),
                ('channel_mkt', models.TextField(blank=True, null=True)),
                ('country_specific', models.JSONField()),
                ('deleted_at', models.DateField(null=True)),
                ('market_group_id', models.TextField(blank=True, null=True)),
                ('market_chain_id', models.TextField(blank=True, null=True)),
                ('created_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', gac.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."customer_typed',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CustomerStaged',
            fields=[
                ('source_id', models.IntegerField()),
                ('price_list', models.IntegerField()),
                ('name', models.TextField()),
                ('dni', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('street', models.TextField(blank=True, null=True)),
                ('street_number', models.TextField(blank=True, null=True)),
                ('location', models.TextField(blank=True, null=True)),
                ('sub_location', models.TextField(blank=True, null=True)),
                ('phone_number', models.TextField(blank=True, null=True)),
                ('business_name', models.TextField(blank=True, null=True)),
                ('category_name', models.TextField(blank=True, null=True)),
                ('category_id', models.TextField(blank=True, null=True)),
                ('main_category_name', models.TextField(blank=True, null=True)),
                ('main_category_id', models.TextField(blank=True, null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('observations', models.TextField(blank=True, null=True)),
                ('credit_amount', models.IntegerField(null=True)),
                ('credit_balance', models.IntegerField(null=True)),
                ('duty_free_price_list', models.IntegerField(null=True)),
                ('zone_id', models.IntegerField()),
                ('route_id', models.IntegerField()),
                ('territory_id', models.IntegerField()),
                ('channel_mkt', models.TextField(blank=True, null=True)),
                ('country_specific', models.JSONField()),
                ('deleted_at', models.DateField(null=True)),
                ('market_group_id', models.TextField(blank=True, null=True)),
                ('market_chain_id', models.TextField(blank=True, null=True)),
                ('created_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', gac.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
                ('branch_office_id', models.ForeignKey(db_column='branch_office_id', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='branch_office.branchofficestaged')),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."customer_staged',
                'managed': True,
            },
        ),
    ]
