import os

RSQLS_DAG_ID = 'run_sqls_dag'
RSQLS_DAG_START_DATE_VALUE = os.environ.get('RSQLS_DAG_START_DATE', '2022-06-20')
RSQLS_DAG_SCHEDULE_INTERVAL = os.environ.get('RSQLS_DAG_SCHEDULE_INTERVAL', None)  # Dag runs manually

SQL_DEPENDENCY_GRAPH = [
    {
        'name': 'calculate_survey_metadata', 'edges': ['get_sovi_calculations'],
    },
    {
        'name': 'get_sovi_calculations', 'edges': [],
    },
    {
        'name': 'clean_answer_mongo', 'edges': [],
    },
    {
        'name': 'create_survey_analysis', 'edges': [],
    },
    {
        'name': 'find_question_id_from_portals', 'edges': [],
    },
    {
        'name': 'find_vendors_with_broken_hierarchy', 'edges': [],
    },
    {
        'name': 'get_aggregated_compliance', 'edges': [],
    },
    {
        'name': 'get_answer_based_data', 'edges': [],
    },
    {
        'name': 'get_edf_calculations', 'edges': [],
    },
    {
        'name': 'get_survey_photo_score', 'edges': ['calculate_survey_metadata', 'get_edf_calculations'],
    },
    {
        'name': 'process_old_survey_data', 'edges': [],
    },
    {
        'name': 'remove_rut_leading_zero', 'edges': [],
    },
    {
        'name': 'update_success_photo_products', 'edges': [],
    },
    {
        'name': 'get_sku_family_compliance', 'edges': [],
    },
]
