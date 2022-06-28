additional_params = {
    'development.surveys.temp': {
        'additional_columns':
        """
            answers_goal_number TEXT,
            country TEXT,
            created_at TEXT,
            is_required TEXT,
            name TEXT,
            paused TEXT,
            portals TEXT,
            updated_at TEXT,
            valid_since TEXT,
            valid_until TEXT,
            workgroup TEXT
        """,
    },
    'development.answers.temp': {
        'additional_columns':
        """
            surveyedId TEXT, -- customerId
            latitude TEXT,
            longitude TEXT,
            skipsSurvey TEXT,
            surveyId TEXT,
            time_elapsed TEXT,
            updatedAt TEXT,
            pollsterId TEXT -- vendorId
        """,
    },
    'staging.surveys.temp': {
        'additional_columns':
        """
            answers_goal_number TEXT,
            country TEXT,
            created_at TEXT,
            is_required TEXT,
            name TEXT,
            paused TEXT,
            portals TEXT,
            updated_at TEXT,
            valid_since TEXT,
            valid_until TEXT,
            workgroup TEXT
        """,
    },
    'staging.answers.temp': {
        'additional_columns':
        """
            surveyedId TEXT, -- customerId
            latitude TEXT,
            longitude TEXT,
            skipsSurvey TEXT,
            surveyId TEXT,
            time_elapsed TEXT,
            updatedAt TEXT,
            pollsterId TEXT -- vendorId
        """,
    },
    'production.surveys.temp': {
        'additional_columns':
        """
            answers_goal_number TEXT,
            created_at TEXT,
            name TEXT,
            paused TEXT,
            portals TEXT,
            updated_at TEXT,
            valid_since TEXT,
            valid_until TEXT
        """,
    },
    'production.answers.temp': {
        'additional_columns':
        """
            latitude TEXT,
            longitude TEXT,
            pollsterId TEXT,
            skipsSurvey TEXT,
            surveyId TEXT,
            surveyedId TEXT,
            time_elapsed TEXT,
            updatedAt TEXT
        """,
    },
}
