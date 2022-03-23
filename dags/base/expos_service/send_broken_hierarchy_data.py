import json

from base.utils.query_with_return import parameterized_query
from base.utils.slack import send_file_content_to_channels


def send_broken_hierarchy_data(job_id):
    data = parameterized_query(f'select * from find_vendors_with_broken_hierarchy({int(job_id)})')
    print(data)
    if len(data) == 0:
        pass  # TODO: send just a message
    else:
        send_file_content_to_channels(file_content=json.dumps(data), channels=['C036G7G8GJ2'],
                                      initial_comment='Aquí está el reporte de vendedores sin supervisor '
                                                      'correspondiente al ETL de hoy :spiral_note_pad:',
                                      title='reporte_vendedores_sin_jerarquia.txt')
