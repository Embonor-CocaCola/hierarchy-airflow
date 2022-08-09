from hierarchy_service.base.utils.query_with_return import parameterized_query
from hierarchy_service.base.utils.slack import send_file_content_to_channels
from hierarchy_service.config.common.settings import SLACK_CHANNEL


def send_broken_hierarchy_data(job_id):
    parameterized_query("analyze airflow.vendor_plant_conform, airflow.vendor_conform, airflow.branch_office_conform")
    data = parameterized_query(f'select * from find_vendors_with_broken_hierarchy({int(job_id)})', wrap=False)
    print(data)
    if len(data) == 0:
        pass  # TODO: send just a message
    else:
        csv_data = 'vendor_source_id,vendor_name,vendor_rut,vendor_email,vendor_phone,branch_office_name,' \
                   'plant_name'
        for row in data:
            csv_data += '\n'
            csv_data += ','.join(map(lambda entry: str(entry), row))
        send_file_content_to_channels(file_content=csv_data, channels=[SLACK_CHANNEL],
                                      initial_comment='Aquí está el reporte de vendedores sin supervisor '
                                                      'correspondiente al ETL de hoy :spiral_note_pad:',
                                      title='reporte_vendedores_sin_jerarquia.csv')
