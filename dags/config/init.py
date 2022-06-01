import logging
import os

from airflow import models
from airflow.settings import Session
from airflow.utils.session import provide_session

import expos_service.settings as es_config
import common.settings as common_config
import success_photo_configuration_load.settings as spcl_config


@provide_session
def _create_connection(conn_id: str = None, uri: str = None, conn_type: str = None, host: str = None,
                       login: str = None, password: str = None, extra=None, session: Session = None):
    connection = session.query(models.Connection).filter_by(
        conn_id=conn_id).first()

    if connection:
        session.delete(connection)
        session.commit()

    try:
        connection = models.Connection(
            conn_id=conn_id,
            uri=uri,
            conn_type=conn_type,
            host=host,
            login=login,
            password=password,
            extra=extra,
        )
        session.add(connection)
        session.commit()
    except Exception as error:
        logging.error(f'Cannot create connection due to {error}')

    session.close()


@provide_session
def _create_pool(name, slots, description, session: Session = None):
    pool = session.query(models.Pool).filter_by(pool=name).first()

    if pool:
        session.delete(pool)
        session.commit()

    try:
        pool = models.Pool()
        pool.pool = name
        pool.slots = slots
        pool.description = description
        session.add(pool)
        session.commit()
    except Exception as error:
        logging.error(f'Cannot create pool due to {error}')

    session.close()


def _initialize(db_config=None, conn_config=None, variable_config=None):
    if db_config is None:
        db_config = {}

    if conn_config is None:
        conn_config = {}

    if variable_config is None:
        variable_config = {}

    logging.info('Configuring airflow connections, pool, and etl tables')

    # DB configuration
    for dag_key, dag_config in db_config.items():
        logging.info(f'Creating configuration for {dag_key}')

        _create_connection(
            conn_id=dag_config.get('conn_id'),
            uri=dag_config.get('conn_uri'),
        )
        _create_pool(
            dag_config.get('pool_id'),
            dag_config.get('pool_task_limit'),
            f'Allows a parallelism limit of {dag_config.get("pool_task_limit")} tasks.',
        )

    # Other connections
    for dag_key, dag_config in conn_config.items():
        logging.info(f'Creating configuration for {dag_key}')

        _create_connection(
            conn_id=dag_config.get('conn_id'),
            uri=dag_config.get('conn_uri'),
            conn_type=dag_config.get('conn_type'),
            host=dag_config.get('conn_host'),
            login=dag_config.get('conn_login'),
            password=dag_config.get('conn_password'),
            extra=dag_config.get('conn_extra'),
        )

    # Variables configuration
    for key, value in variable_config.items():
        models.Variable.set(key, value)


if __name__ == '__main__':
    _db_config = {
    }
    _conn_config = {
        es_config.ES_EMBONOR_SERVICES_BASE_URL_CONN_ID: {
            'conn_id': es_config.ES_EMBONOR_SERVICES_BASE_URL_CONN_ID,
            'conn_type': 'http',
            'conn_host': es_config.ES_EMBONOR_SERVICES_BASE_URL,
        },
        es_config.ES_EMBONOR_PG_CONN_ID: {
            'conn_id': es_config.ES_EMBONOR_PG_CONN_ID,
            'conn_uri': es_config.ES_EMBONOR_PG_CONN_URI,
        },
        es_config.ES_AIRFLOW_DATABASE_CONN_ID: {
            'conn_id': es_config.ES_AIRFLOW_DATABASE_CONN_ID,
            'conn_uri': es_config.ES_AIRFLOW_DATABASE_CONN_URI,
        },
        es_config.ES_SSH_CONN_ID: {
            'conn_id': es_config.ES_SSH_CONN_ID,
            'conn_uri': es_config.ES_SSH_CONN_URI,
        },
        es_config.ES_EMBONOR_MONGO_CONN_ID: {
            'conn_id': es_config.ES_EMBONOR_MONGO_CONN_ID,
            'conn_uri': es_config.ES_EMBONOR_MONGO_CONN_URI,
        },
        common_config.EXPOS_DATABASE_CONN_ID: {
            'conn_id': common_config.EXPOS_DATABASE_CONN_ID,
            'conn_uri': os.environ.get('EXPOS_SQL_CONN_URI'),
        },
        spcl_config.SPCL_S3_CONN_ID: {
            'conn_id': spcl_config.SPCL_S3_CONN_ID,
            'conn_uri': os.environ.get('SPCL_S3_CONN_URI'),
        },
    }
    _variable_config = {
        'ml_auth_token': '6362F8A5-F441-4943-9C81-3D96229E8BDE',
        es_config.ES_FETCH_OLD_EVALUATIONS_KEY: False,
    }
    _initialize(_db_config, _conn_config, _variable_config)
