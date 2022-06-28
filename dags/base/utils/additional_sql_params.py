additional_params = {
    'development.surveys.temp': {
        'additional_columns':
        """
            created_at TEXT,
            name TEXT,
            paused TEXT,
            period TEXT,
            portals TEXT,
            updated_at TEXT,
            valid_since TEXT,
            valid_until TEXT
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
}
