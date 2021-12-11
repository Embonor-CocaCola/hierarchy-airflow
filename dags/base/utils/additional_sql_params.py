additional_params = {
    'development.questions.temp': {
        'additional_columns': 'observation TEXT,',
    },
    'staging.questions.temp': {
        'additional_columns': '',
    },
    'production.questions.temp': {
        'additional_columns': '',
    },
    'development.questions.typed': {
        'date_cast': ", 'YYYY-MM-DD HH24:MI:SS'",
    },
    'staging.questions.typed': {
        'date_cast': ':: BIGINT',
    },
    'production.questions.typed': {
        'date_cast': ':: BIGINT',
    },
    'development.answer.typed': {
        'date_cast': ", 'YYYY-MM-DD HH24:MI:SS'",
    },
    'staging.answer.typed': {
        'date_cast': ':: BIGINT',
    },
    'production.answer.typed': {
        'date_cast': ':: BIGINT',
    },
    'development.survey.typed': {
        'date_cast': ", 'YYYY-MM-DD HH24:MI:SS'",
    },
    'staging.survey.typed': {
        'date_cast': ':: BIGINT',
    },
    'production.survey.typed': {
        'date_cast': ':: BIGINT',
    },
}
