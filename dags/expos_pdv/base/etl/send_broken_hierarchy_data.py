from expos_pdv.base.utils.query_with_return import parameterized_query
from expos_pdv.base.utils.slack import send_file_content_to_channels
from expos_pdv.config.common.settings import SLACK_ETL_SUCCESS_CHANNEL


def send_broken_hierarchy_data(job_id):
    data = parameterized_query(f'select * from find_vendors_with_broken_hierarchy({int(job_id)})', wrap=False)
    print(data)
    if len(data) == 0:
        pass  # TODO: send just a message
    else:
        csv_data = 'vendor_source_id,vendor_name,vendor_rut,vendor_email,vendor_phone,branch_office_name,' \
                   'plant_name,last_evaluation_at,evaluations_total'
        for row in data:
            csv_data += '\n'
            csv_data += ','.join(map(lambda entry: str(entry), row))
        send_file_content_to_channels(file_content=csv_data, channels=[SLACK_ETL_SUCCESS_CHANNEL],
                                      initial_comment='Aquí está el reporte de vendedores sin supervisor '
                                                      'correspondiente al ETL de hoy :spiral_note_pad:',
                                      title='reporte_vendedores_sin_jerarquia.csv')
