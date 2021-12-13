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
    'development.question.typed': {
        'date_cast': ', \'YYYY-MM-DD"T"HH24:MI:SS"Z"\'',
    },
    'staging.question.typed': {
        'date_cast': ':: BIGINT',
    },
    'production.question.typed': {
        'date_cast': ':: BIGINT',
    },
    'development.answer.typed': {
        'date_cast': ', \'YYYY-MM-DD"T"HH24:MI:SS"Z"\'',
    },
    'staging.answer.typed': {
        'date_cast': ':: BIGINT',
    },
    'production.answer.typed': {
        'date_cast': ':: BIGINT',
    },
    'development.survey.typed': {
        'date_cast': ', \'YYYY-MM-DD"T"HH24:MI:SS"Z"\'',
    },
    'staging.survey.typed': {
        'date_cast': ':: BIGINT',
    },
    'production.survey.typed': {
        'date_cast': ':: BIGINT',
    },
}
