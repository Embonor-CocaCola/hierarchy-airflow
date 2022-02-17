additional_params = {
    'development.questions.temp': {
        'additional_columns': 'observation TEXT,',
    },
    'staging.questions.temp': {
        'additional_columns': '',
    },
    'production.questions.temp': {
        'additional_columns': 'observation TEXT,',
    },
    'development.surveys.temp': {
        'additional_columns':
        """
            created_at TEXT,
            name TEXT,
            paused TEXT,
            period TEXT,
        """,
    },
    'staging.surveys.temp': {
        'additional_columns':
        """
            answers_goal_number TEXT,
            created_at TEXT,
            name TEXT,
            paused TEXT,
        """,
    },
    'production.surveys.temp': {
        'additional_columns':
        """
            answers_goal_number TEXT,
            created_at TEXT,
            name TEXT,
            paused TEXT,
        """,
    },
}
