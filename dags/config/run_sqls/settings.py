import os

RSQLS_DAG_ID = 'run_sqls_dag'
RSQLS_DAG_START_DATE_VALUE = os.environ.get('RSQLS_DAG_START_DATE', '2022-06-20')
RSQLS_DAG_SCHEDULE_INTERVAL = os.environ.get('RSQLS_DAG_SCHEDULE_INTERVAL', None)  # Dag runs manually

#  Adjacency list indicaating dependency of a sql script from other sql scripts.
#  'edges' indicate dependency, e.g. if a sql named A has B in its edges, B must be executed first (A depends on B)
#  in other words, A "uses" B.
SQL_DEPENDENCY_GRAPH = [
    {
        'name': 'calculate_survey_metadata', 'edges': ['get_sovi_calculations'],
    },
    {
        'name': 'get_sovi_calculations', 'edges': [], 'refresh_data': [{'table_name': 'preprocessed_sovi'}],
    },
    {
        'name': 'clean_answer_mongo', 'edges': ['stringify_oid'],
    },
    {
        'name': 'clean_survey_mongo', 'edges': ['stringify_oid'],
    },
    {
        'name': 'create_survey_analysis', 'edges': [],
    },
    {
        'name': 'find_question_id_from_portals', 'edges': ['stringify_oid'],
    },
    {
        'name': 'find_vendors_with_broken_hierarchy', 'edges': [],
    },
    {
        'name': 'get_aggregated_compliance',
        'edges': ['get_sku_family_compliance'],
        'refresh_data': [{'table_name': 'preprocessed_success_photo'}, {'table_name': 'preprocessed_essentials'}],
    },
    {
        'name': 'get_answer_based_data', 'edges': [], 'refresh_data': [{'table_name': 'preprocessed_answers'}],
    },
    {
        'name': 'get_edf_calculations', 'edges': [], 'refresh_data': [{'table_name': 'preprocessed_edf'}],
    },
    {
        'name': 'get_survey_photo_score',
        'edges': ['calculate_survey_metadata', 'get_edf_calculations'],
        'refresh_data': [{'table_name': 'survey_photo_score'}],
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
        'name': 'get_sku_family_compliance',
        'edges': [],
        'refresh_data': [{'table_name': 'sku_family_compliance'}],
    },
    {
        'name': 'stringify_oid',
        'edges': [],
    },
]
