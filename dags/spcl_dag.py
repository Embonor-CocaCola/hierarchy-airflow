from airflow import DAG
from base.success_photo_configuration_load.success_photo_configuration_load_dag_factory import (
    SuccessPhotoConfigurationLoadDagFactory,
)

dag: DAG = SuccessPhotoConfigurationLoadDagFactory.build()
